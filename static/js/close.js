export const Close = () => {
  const menu = document.querySelector("#menu");
  const open_button = document.querySelector("#open_button");
  const close_button = document.querySelector("#close_button");


  menu.style.display = 'none';
  open_button.style.display = 'flex';
  close_button.style.display = 'none';
}
