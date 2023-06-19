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
			content = `<a href="${href}" title="${title}">${prompt(
				prompt_message
			)}</a>`;
		} else content = `<${tag}>${prompt(prompt_message)}</${tag}>`;

		textarea.value += content;
		e.preventDefault();
	});
	btns_panel.appendChild(button);
}
html_btns_panel.appendChild(btns_panel);
textarea.after(html_btns_panel);
