const API = "http://127.0.0.1:8000";
const STATUSES = ["Applied", "OA", "Interview", "Offer", "Rejected"];

const list = document.getElementById("list");
const form = document.getElementById("app-form");

async function loadApplications() {
  const res = await fetch(`${API}/applications`);
  const apps = await res.json();

  list.innerHTML = "";
  if (apps.length === 0) {
    list.textContent = "No applications yet.";
    return;
  }
  apps.forEach((a) => list.appendChild(buildCard(a)));
}

function buildCard(a) {
  const card = document.createElement("div");
  card.className = "card";

  const title = document.createElement("h3");
  title.textContent = `${a.company} — ${a.role}`;

  const meta = document.createElement("p");
  meta.textContent = [a.applied_date, a.notes].filter(Boolean).join(" · ");

  const select = document.createElement("select");
  STATUSES.forEach((s) => {
    const option = document.createElement("option");
    option.value = s;
    option.textContent = s;
    if (s === a.status) option.selected = true;
    select.appendChild(option);
  });
  select.addEventListener("change", () => updateStatus(a, select.value));

  const del = document.createElement("button");
  del.textContent = "Delete";
  del.addEventListener("click", () => deleteApplication(a.id));

  card.append(title, meta, select, del);
  return card;
}

async function updateStatus(a, newStatus) {
  await fetch(`${API}/applications/${a.id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      company: a.company,
      role: a.role,
      status: newStatus,
      applied_date: a.applied_date,
      notes: a.notes,
    }),
  });
  loadApplications();
}

async function deleteApplication(id) {
  await fetch(`${API}/applications/${id}`, { method: "DELETE" });
  loadApplications();
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const data = {
    company: document.getElementById("company").value,
    role: document.getElementById("role").value,
    status: document.getElementById("status").value,
    applied_date: document.getElementById("applied_date").value || null,
    notes: document.getElementById("notes").value || null,
  };
  await fetch(`${API}/applications`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  form.reset();
  loadApplications();
});

loadApplications();