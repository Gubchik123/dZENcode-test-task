const BOOTSTRAP_5_MD_BREAKPOINT = 768; // px
const BOOTSTRAP_5_LG_BREAKPOINT = 992; // px

const order_by_btn = document.querySelector(".dropdown-toggle");
const order_dir_btn = document.querySelector(".btn-group");
const pagination = document.querySelector(".pagination");

function resize() {
	if (window.outerWidth >= BOOTSTRAP_5_LG_BREAKPOINT) {
		order_by_btn.classList.add("btn-lg");
		order_dir_btn.classList.add("btn-group-lg");
		if (pagination) pagination.classList.add("pagination-lg");
	} else {
		order_by_btn.classList.remove("btn-lg");
		order_dir_btn.classList.remove("btn-group-lg");
		if (pagination) pagination.classList.remove("pagination-lg");
	}

	if (window.outerWidth <= BOOTSTRAP_5_MD_BREAKPOINT) {
		order_by_btn.classList.add("btn-sm");
		order_dir_btn.classList.add("btn-group-sm");
		if (pagination) pagination.classList.add("pagination-sm");
	} else {
		order_by_btn.classList.remove("btn-sm");
		order_dir_btn.classList.remove("btn-group-sm");
		if (pagination) pagination.classList.remove("pagination-sm");
	}
}

resize();
window.addEventListener("resize", resize);
