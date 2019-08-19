// @flow
import { buildReq } from "../../../../../dalite/static/js/ajax.js";

/*********/
/* model */
/*********/

type Collection = {
  title: string,
  description: string,
  discipline: string,
  nAssignments: number,
  nFollowers: number,
};

let model: {
  collections: Array<Collection>,
  urls: {
    collections: string,
  },
};

function initModel(data: { urls: { collections: string } }) {
  model = {
    collections: [],
    urls: {
      collections: data.urls.collections,
    },
  };
}

type Rationale = {
  title: string,
  description: string,
  answer: string,
  score: number,
  annotator: number,
};

let model: {
  rationales: Array<Rationale>,
  urls: {
    rationales: string,
  },
};

function initModel(data: { urls: { rationales: string } }) {
  model = {
    rationales: [],
    urls: {
      rationales: data.urls.rationales,
    },
  };
}

/**********/
/* update */
/**********/

async function update() {
  await getCollections();
  await getRationales();
}

async function getCollections() {
  const data = {};
  const req = buildReq(data, "post");
  const resp = await fetch(model.urls.collections, req);
  const json = await resp.json();
  model.collections = json.collections.map(collection => ({
    title: collection.title,
    description: collection.description,
    discipline: collection.discipline,
    nAssignments: collection.n_assignments,
    nFollowers: collection.n_followers,
  }));
  collectionsView();
}

async function getRationales() {
  const data = {};
  const req = buildReq(data, "post");
  const resp = await fetch(model.urls.rationales, req);
  const json = await resp.json();
  model.rationales = json.rationales.map(rationale => ({
    qTitle: rationale.title,
    rationale: rationale.rationale,
    choice: rationale.choice,
    choiceText: rationale.text,
    correct: rationale.correct,
  }));
  rationalesView();
}

/********/
/* view */
/********/

function collectionsView() {
  const section = document.querySelector(".collections");
  if (!section) {
    throw new Error("There is a missing section with class `collections`");
  }
  if (model.collections.length) {
    section.classList.remove("collections--hidden");
  } else {
    section.classList.add("collections--hidden");
  }
}

function rationalesView() {
  const section = document.querySelector(".rationales");
  if (!section) {
    throw new Error("There is a missing section with class `rationales`");
  }
  if (model.rationales.length) {
    section.classList.remove("rationales--hidden");
  } else {
    section.classList.add("rationales--hidden");
  }
}

/********/
/* init */
/********/

export async function init(data: { urls: { collections: string } }) {
  initModel(data);
  await update();
}
