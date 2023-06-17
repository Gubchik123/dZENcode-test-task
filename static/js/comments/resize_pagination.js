const pagination = document.querySelector(".pagination");

function resize_pagination_nav() {
	window.outerWidth >= 992
		? pagination.classList.add("pagination-lg")
		: pagination.classList.remove("pagination-lg");

	window.outerWidth <= 768
		? pagination.classList.add("pagination-sm")
		: pagination.classList.remove("pagination-sm");
}

if (pagination) {
	resize_pagination_nav();
	window.addEventListener("resize", resize_pagination_nav);
}