async function loadResume() {
  const res = await fetch("/api/resume");
  const data = await res.json();
  const p = data.profile;
  document.getElementById("resume-app").innerHTML = `
    <h1>${p.name}</h1>
    <div class="contact">${p.email} · ${p.phone} · <a href="${p.linkedin}">LinkedIn</a> · <a href="${p.github}">GitHub</a></div>
    <p>${p.summary}</p>
    <h2>Experience</h2>
    ${data.experience.map(e => `
      <div class="item"><strong>${e.role}</strong> — ${e.company}
      <div class="meta">${e.duration}</div>
      <ul>${e.highlights.map(h => `<li>${h}</li>`).join("")}</ul></div>`).join("")}
    <h2>Projects</h2>
    ${data.projects.map(pr => `
      <div class="item"><strong>${pr.title}</strong> <span class="meta">(${pr.stack})</span>
      <div>${pr.description}</div></div>`).join("")}
    <h2>Education</h2>
    ${data.education.map(ed => `
      <div class="item"><strong>${ed.institution}</strong> — ${ed.degree}
      <div class="meta">${ed.duration} · ${ed.score}</div></div>`).join("")}
    <h2>Skills</h2>
    <div class="skills">${data.skills.map(s => `<span>${s}</span>`).join("")}</div>
  `;
}
loadResume();

const history = [];
const log = document.getElementById("log");

function render(role, text) {
  const div = document.createElement("div");
  div.className = "msg " + (role === "user" ? "user" : "bot");
  div.textContent = text;
  log.appendChild(div);
  log.scrollTop = log.scrollHeight;
}

document.getElementById("chat-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const input = document.getElementById("chat-input");
  const text = input.value.trim();
  if (!text) return;
  input.value = "";
  render("user", text);
  history.push({ role: "user", content: text });

  const res = await fetch("/api/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ messages: history }),
  });
  const data = await res.json();
  const answer = data.answer ?? data.error ?? "Something went wrong.";
  render("assistant", answer);
  history.push({ role: "assistant", content: answer });
});