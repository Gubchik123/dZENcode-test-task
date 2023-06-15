const go_to_top_btn = document.getElementById("go-to-top-btn");
go_to_top_btn.addEventListener("click", function () {
	document.body.scrollTop = 0; // For Safari
	document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE and
});

function check_window_size() {
	// When the user scrolls down 200px from the top of the document, show the button
	if (
		document.body.scrollTop > 200 ||
		document.documentElement.scrollTop > 200
	)
		go_to_top_btn.classList = "d-flex content-center";
	else go_to_top_btn.classList = "";
}

window.addEventListener("scroll", check_window_size);

check_window_size();
