const TRASH_ICON =
  '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M9 3h6l1 2h4v2H4V5h4l1-2zm-3 6h12l-1 12H7L6 9z"/></svg>';

export function renderTodos(list, todos, { onToggle, onDelete }) {
  list.innerHTML = "";
  todos.forEach((todo) => {
    const li = document.createElement("li");
    if (todo.done) li.className = "done";

    const dot = document.createElement("button");
    dot.className = "dot";
    dot.setAttribute("aria-label", todo.done ? "Mark as not done" : "Mark as done");
    dot.addEventListener("click", () => onToggle(todo.id));

    const label = document.createElement("span");
    label.className = "todo-title";
    label.textContent = todo.title;

    const delBtn = document.createElement("button");
    delBtn.className = "del-btn";
    delBtn.setAttribute("aria-label", "Delete task");
    delBtn.innerHTML = TRASH_ICON;
    delBtn.addEventListener("click", () => onDelete(todo.id));

    li.append(dot, label, delBtn);
    list.appendChild(li);
  });
}
