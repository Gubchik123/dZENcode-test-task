const url_params = new URLSearchParams(window.location.search);

const order_by = url_params.get("orderby") || "c";
const order_dir = url_params.get("orderdir") || "desc";

// Script to add .active class for dropdown-item
const dropdown_items = document.querySelectorAll(".dropdown-item");

let index = { u: 0, e: 1, c: 2 }[order_by];
dropdown_items[index].classList.add("active");

// Script to add .active class for btn of btn-group
const btns_of_btn_group = document.querySelectorAll(".btn-group > .btn");

index = { asc: 0, desc: 1 }[order_dir];
btns_of_btn_group[index].classList.add("active");
