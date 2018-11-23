# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import base64
from django.db import models
from django.utils.translation import ugettext_lazy as _


class StudentGroup(models.Model):
    name = models.CharField(max_length=100, unique=True)
    title = models.CharField(max_length=100, null=True, blank=True)
    creation_date = models.DateField(blank=True, null=True, auto_now=True)
    teacher = models.ManyToManyField("Teacher", blank=True)
    student_school_id_needed = models.BooleanField(default=False)

    def __unicode__(self):
        if not self.title:
            return self.name
        else:
            return self.title

    class Meta:
        ordering = ["-creation_date"]
        verbose_name = _("group")
        verbose_name_plural = _("groups")

    @staticmethod
    def get(hash_):
        assert isinstance(hash_, basestring), "Precondition failed for `hash_`"
        try:
            id_ = int(base64.urlsafe_b64decode(hash_.encode()).decode())
        except UnicodeDecodeError:
            id_ = None
        if id_:
            try:
                group = StudentGroup.objects.get(id=id_)
            except StudentGroup.DoesNotExist:
                group = None
        else:
            group = None

        output = group
        assert output is None or isinstance(
            output, StudentGroup
        ), "Postcondition failed"
        return output

    @property
    def hash(self):
        output = base64.urlsafe_b64encode(str(self.id).encode()).decode()
        assert isinstance(output, basestring), "Postcondition failed"
        return output

    @property
    def students(self):
        return self.student_set.all()

    @property
    def has_emails(self):
        return all(s.student.email for s in self.students)
