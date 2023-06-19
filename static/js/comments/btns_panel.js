const textarea = document.getElementById("id_text");

const html_btns_panel = document.createElement("div");
html_btns_panel.innerHTML = "Allowed HTML tags:";
html_btns_panel.classList = "w-100 d-flex content-between mb-2";
html_btns_panel.id = "btns_panel";

const btns_panel = document.createElement("div");

for (const tag of ["a", "code", "i", "strong"]) {
	const button = document.createElement("button");
	button.classList = "btn btn-sm btn-primary me-1";
	button.textContent = tag;

	button.addEventListener("click", function (e) {
		let content = "";
		const prompt_message = `Enter content for <${tag}> tag:`;

		if (tag === "a") {
			const href = prompt("Enter href for <a> tag:");
			const title = prompt("Enter title for <a> tag:");
			const user_answer = prompt(prompt_message);

			if (!href || !title || !user_answer) {
				e.preventDefault();
				return;
			}
			content = `<a href="${href}" title="${title}">${user_answer}</a>`;
		} else {
			const user_answer = prompt(prompt_message);

			if (!user_answer) {
				e.preventDefault();
				return;
			}
			content = `<${tag}>${user_answer}</${tag}>`;
		}

		textarea.value += content;
		e.preventDefault();
	});
	btns_panel.appendChild(button);
}
html_btns_panel.appendChild(btns_panel);
textarea.after(html_btns_panel);
