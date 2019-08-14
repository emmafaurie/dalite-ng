# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from itertools import chain

from django.db import models

from criterion_list import get_criterion

from ..logger import logger


class ReputationType(models.Model):
    type = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.type

    def _calculate_points(self, criterion, model):
        """
        Calculates the number of points returned by the model based on the
        criterion evaluation and its point thresholds.

        Parameters
        ----------
        criterion : Criterion
            Criterion used for the evaluation
        model : Union[Question, Assignment, Teacher]
            Model for which to evaluate the reputation

        Returns
        -------
        Dict[str, Any]
            Reputation as evaluated by the criterion as
            {
                reputation: float,
                details: Dict[str, Any]
            }

        Raises
        ------
        TypeError
            If the given `model` doesn't correspond to the `type`
        """
        evaluation, details = criterion.evaluate(model)

        if criterion.thresholds:
            points = sum(
                float(points_)
                * (min(evaluation, float(threshold)) - float(prev_threshold))
                for points_, threshold, prev_threshold in zip(
                    criterion.points_per_threshold,
                    criterion.thresholds,
                    [0] + criterion.thresholds[:-1],
                )
            )
            if len(criterion.points_per_threshold) > len(criterion.thresholds):
                points = points + float(
                    criterion.points_per_threshold[-1]
                ) * max(0, evaluation - float(criterion.thresholds[-1]))

        else:
            points = float(criterion.points_per_threshold[0]) * evaluation

        return {"reputation": points, "details": details}

    def evaluate(self, model, criterion=None):
        """
        Returns the reputation of the linked model as a tuple of the quality
        and the different criterion results.

        Parameters
        ----------
        model : Union[Question, Assignment, Teacher]
            Model for which to evaluate the reputation
        criterion : Optional[str] (default : None)
            Name of the criterion for which reputation is calculated. If None,
            evaluates for all criteria

        Returns
        -------
        Optional[float]
            Quality of the answer or None of no criteria present
        Either
            List[Dict[str, Any]]
                If `criterion` is None, individual criteria under the format
                    [{
                        name: str
                        full_name: str
                        description: str
                        version: int
                        weight: int
                        reputation: float
                    }]
            Dict[str, Any]
                If `criterion` is specified, details under the format
                    {
                        name: str
                        full_name: str
                        description: str
                        version: int
                        weight: int
                        reputation: float
                    }

        Raises
        ------
        TypeError
            If the given `model` doesn't correspond to the `type`
        """
        if model.__class__.__name__.lower() != self.type:
            msg = (
                "The type of `model` doesn't correspond to the correct "
                "type; is {} instead of {}.".format(
                    model.__class__.__name__.lower(), self.type
                )
            )
            logger.error("TypeError: {}".format(msg))
            raise TypeError(msg)

        if not self.criteria.exists():
            return None, []

        if criterion is None:
            reputations = [
                dict(
                    chain(
                        self._calculate_points(criterion_, model).items(),
                        criterion_.__iter__(),
                    )
                )
                for criterion_ in (
                    get_criterion(c.name).objects.get(version=c.version)
                    for c in self.criteria.all()
                )
            ]
            reputation = sum(r["reputation"] for r in reputations)
        else:
            try:
                criterion_ = next(
                    c for c in self.criteria.all() if c.name == criterion
                )
            except StopIteration:
                msg = "The criterion {} isn't part of the criteria".format(
                    criterion
                ) + " for reputation_type {}.".format(self.type)
                logger.error("ValueError: {}".format(msg))
                raise ValueError(msg)

            reputations = dict(
                chain(
                    self._calculate_points(criterion_, model).items(),
                    criterion_.__iter__(),
                )
            )
            reputation = reputations["reputation"]

        return reputation, reputations


class UsesCriterion(models.Model):
    reputation_type = models.ForeignKey(
        ReputationType, related_name="criteria"
    )
    name = models.CharField(max_length=32)
    version = models.PositiveIntegerField()

    def __iter__(self):
        criterion_class = get_criterion(self.name)
        criterion = criterion_class.objects.get(version=self.version)
        return iter(criterion)

    def __str__(self):
        return "{} for reputation type {}".format(
            self.name, str(self.reputation_type)
        )
