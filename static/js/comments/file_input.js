const file_input = document.getElementById("id_file");
const file_preview = document.getElementById("file-preview");
const image_preview = document.getElementById("image-preview");
const resized_image_input = document.getElementById("resized_image");

image_preview.addEventListener("click", function () {
	const modal = new bootstrap.Modal(
		document.getElementById("preview-image-modal")
	);
	modal.show();
});

file_input.addEventListener("change", function () {
	file_preview.innerHTML = "";

	const file = file_input.files[0];

	if (file) {
		const file_type = file.type;

		if (file_type.startsWith("image/")) {
			const image_type = file_type.split("/")[1];
			if (
				!["jpeg", "jpg", "gif", "png"].includes(
					image_type.toLowerCase()
				)
			) {
				file_input.value = "";
				alert(
					"Please select an image file in JPEG, JPG, GIF, or PNG format."
				);
				return;
			}
			process_image(file);
		} else if (file_type === "text/plain") {
			const MAX_FILE_SIZE = 100 * 1024; // 100 KB

			if (file.size > MAX_FILE_SIZE) {
				file_input.value = "";
				alert("Text file size exceeds the maximum limit (100 KB).");
			}
		} else {
			file_input.value = "";
			alert(
				"Please select a file in JPEG, JPG, GIF, PNG, or TXT format."
			);
		}
	}
});

function process_image(file) {
	const reader = new FileReader();
	reader.onload = function (e) {
		const img = document.createElement("img");
		img.onload = function (event) {
			const MAX_WIDTH = 320;
			const MAX_HEIGHT = 240;

			let width = img.width;
			let height = img.height;

			if (width > MAX_WIDTH || height > MAX_HEIGHT) {
				const width_ratio = MAX_WIDTH / width;
				const height_ratio = MAX_HEIGHT / height;
				const scale_factor = Math.min(width_ratio, height_ratio);
				width = Math.floor(width * scale_factor);
				height = Math.floor(height * scale_factor);
			}

			const canvas = document.createElement("canvas");
			canvas.width = width;
			canvas.height = height;
			const ctx = canvas.getContext("2d");
			ctx.drawImage(img, 0, 0, width, height);

			const data_url = canvas.toDataURL(file.type);
			image_preview.src = data_url;
			resized_image_input.value = data_url;
			file_preview.innerHTML = `<img src="${data_url}" alt="Image preview"/>`;
		};
		img.src = e.target.result;
	};
	reader.readAsDataURL(file);
}
