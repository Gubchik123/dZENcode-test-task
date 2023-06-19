// ! const textarea has already been declared
const form = document.getElementById("comment_form");

form.addEventListener("keypress", function (event) {
	if (event.key === "Enter") event.preventDefault();
});

function has_unclosed_tags(text) {
	const unclosed_tags = text.match(/<(\w+)(?!.*<\/\1)/g);
	if (unclosed_tags) {
		alert(
			"Please close the following HTML tags: " + unclosed_tags.join(", ")
		);
		return false;
	}
	return true;
}

function is_valid_tags(text) {
	const allowed_tags = ["a", "code", "i", "strong"];
	const invalid_tags = text.match(/<(\/)?(\w+)[^>]*>/g);
	if (invalid_tags) {
		for (const i = 0; i < invalid_tags.length; i++) {
			const tag = invalid_tags[i].replace(/<\/?(\w+)[^>]*>/g, "$1");
			if (allowed_tags.indexOf(tag) === -1) {
				alert(
					"Invalid tags detected. Only 'a', 'code', 'i', 'strong' tags are allowed."
				);
				return false;
			}
		}
	}
	return true;
}

const submit_btn = document.getElementById("submit_btn");
submit_btn.addEventListener("click", function (event) {
	const textarea_value = textarea.value;

	if (!has_unclosed_tags(textarea_value) || !is_valid_tags(textarea_value)) {
		event.preventDefault();
		return;
	}
});
