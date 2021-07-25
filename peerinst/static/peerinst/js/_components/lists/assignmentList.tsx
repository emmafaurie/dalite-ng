import { Fragment, h } from "preact";

import { IconButton } from "@rmwc/icon-button";
import {
  List,
  ListDivider,
  ListItem,
  ListItemGraphic,
  ListItemText,
  ListItemPrimaryText,
  ListItemSecondaryText,
} from "@rmwc/list";

import { Info } from "../question";

import "@rmwc/icon-button/node_modules/@material/icon-button/dist/mdc.icon-button.min.css";
import "@rmwc/list/node_modules/@material/list/dist/mdc.list.css";

export type Assignment = {
  editable: boolean;
  is_valid: boolean; // eslint-disable-line camelcase
  pk: string;
  question_pks: number[]; // eslint-disable-line camelcase
  title: string;
  urls: {
    copy: string;
    distribute: string;
    fix: string;
    preview: string;
    update: string;
  };
};

type AssignmentListProps = {
  archived: Assignment[];
  assignments: Assignment[];
  gettext: (a: string) => string;
  handleToggleArchived: (a: Assignment) => Promise<void>;
  ownedAssignments: Assignment[];
  view: string;
};

export function AssignmentList({
  archived,
  assignments,
  gettext,
  handleToggleArchived,
  ownedAssignments,
  view,
}: AssignmentListProps): JSX.Element {
  console.debug(
    archived,
    assignments,
    gettext,
    handleToggleArchived,
    ownedAssignments,
    view,
  );
  const archivedPks = archived.map((a) => a.pk);
  const ownedPks = ownedAssignments.map((a) => a.pk);

  const sort = (a: Assignment, b: Assignment): number => {
    // Triple sort on owned, then editable, then title
    if (+ownedPks.includes(b.pk) == +ownedPks.includes(a.pk)) {
      if (a.editable == b.editable || !ownedPks.includes(b.pk)) {
        return a.title.localeCompare(b.title);
      }
      return +b.editable - +a.editable;
    }
    return +ownedPks.includes(b.pk) - +ownedPks.includes(a.pk);
  };

  const info = (): JSX.Element | undefined => {
    if (assignments.length == 0 && view == "") {
      return (
        <Info
          className="large"
          text={gettext(
            "You are not currently following any assignments.  You can create one, search for one in the database, or unarchive an old one.",
          )}
          type="alert"
        />
      );
    }
    if (view == "") {
      return (
        <Info
          className="large"
          text={gettext(
            "This is the list of assignments you have authored or are currently following, and for which reports will be available.  You can archive or unfollow any assignments you are no longer using.",
          )}
          type="tip"
        />
      );
    }
    if (view == "archived") {
      return (
        <Info
          className="large"
          text={gettext(
            "This is the list of assignments you have authored and archived.",
          )}
          type="tip"
        />
      );
    }
    return;
  };

  return (
    <Fragment>
      <div style={{ marginBottom: 8, maxWidth: 600 }}>{info()}</div>
      <List twoLine>
        {assignments
          .concat(archived)
          .sort(sort)
          .filter((a) => {
            return view == "archived"
              ? archivedPks.includes(a.pk)
              : !archivedPks.includes(a.pk);
          })
          .map((a: Assignment, i: number) => {
            return (
              <div key={i}>
                <AssignmentListItem
                  archived={archivedPks.includes(a.pk)}
                  assignment={a}
                  gettext={gettext}
                  handleToggleArchived={handleToggleArchived}
                  owned={ownedPks.includes(a.pk)}
                />
              </div>
            );
          })}
        <ListDivider />
      </List>
    </Fragment>
  );
}

type AssignmentListItemProps = {
  archived: boolean;
  assignment: Assignment;
  gettext: (a: string) => string;
  handleToggleArchived: (a: Assignment) => Promise<void>;
  owned: boolean;
};

function AssignmentListItem({
  archived,
  assignment,
  gettext,
  handleToggleArchived,
  owned,
}: AssignmentListItemProps): JSX.Element {
  const archiveIcon = (): JSX.Element | undefined => {
    return (
      <IconButton
        icon={
          owned && archived ? "unarchive" : owned ? "archive" : "remove_circle"
        }
        onClick={() => handleToggleArchived(assignment)}
        title={
          archived
            ? gettext("Unarchive this assignment.")
            : owned
            ? gettext("Archive this assignment to hide it.")
            : gettext("Unfollow this assignment.")
        }
      />
    );
  };

  const editIcon = (): JSX.Element | undefined => {
    const edit = owned && assignment.editable;
    if (!archived) {
      return (
        <IconButton
          icon={edit ? "edit" : "file_copy"}
          onClick={() =>
            (window.location.href = edit
              ? assignment.urls.update
              : assignment.urls.copy)
          }
          title={
            edit
              ? gettext("Edit this assignment to make changes.")
              : gettext("Copy this assignment to make changes.")
          }
        />
      );
    }
  };

  const distributeIcon = (): JSX.Element | undefined => {
    if (!archived && assignment.is_valid) {
      return (
        <IconButton
          icon="share"
          onClick={() => (window.location.href = assignment.urls.distribute)}
          title={gettext("Distribute this assignment to one of your groups.")}
        />
      );
    }
  };

  const icons = () => {
    return (
      <div style={{ marginLeft: "auto" }}>
        {distributeIcon()}
        {editIcon()}
        {archiveIcon()}
      </div>
    );
  };

  const caption = (): JSX.Element => {
    console.debug(assignment);
    if (assignment.is_valid) {
      return (
        <span>
          {assignment.question_pks.length} {gettext("questions")}
        </span>
      );
    }
    return (
      <span style={{ color: "var(--mdc-theme-error)" }}>
        {gettext("There is a problem with this assignment.")}
      </span>
    );
  };

  return (
    <Fragment>
      <ListDivider />
      <ListItem
        className={
          archived ? "question-list-item hatched" : "question-list-item"
        }
      >
        <ListItemGraphic
          icon={assignment.is_valid ? "assignment" : "report"}
          onClick={() =>
            (window.location.href = assignment.is_valid
              ? assignment.urls.preview
              : assignment.urls.fix)
          }
          style={{ cursor: "pointer", fontSize: 36 }}
          theme={assignment.is_valid ? "primary" : "error"}
        />
        <ListItemText>
          <ListItemPrimaryText
            onClick={() =>
              (window.location.href = assignment.is_valid
                ? assignment.urls.preview
                : assignment.urls.fix)
            }
            style={{ cursor: "pointer", fontWeight: "bold" }}
            theme={assignment.is_valid ? "secondary" : "error"}
          >
            {assignment.title}
          </ListItemPrimaryText>
          <ListItemSecondaryText theme="textHintOnBackground">
            {caption()}
          </ListItemSecondaryText>
        </ListItemText>
        {icons()}
      </ListItem>
    </Fragment>
  );
}
