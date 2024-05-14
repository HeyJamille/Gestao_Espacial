export const Open = () => {
  const menu = document.querySelector("#menu");
  const nav = document.querySelector("#nav");
  const button = document.querySelector("#button");
  const open_button = document.querySelector("#open_button");
  const close_button = document.querySelector("#close_button");


  menu.style.display = 'flex';
  nav.style.flexDirection = 'column';
  button.style.justifyContent = 'end';


  open_button.style.display = 'none';
  close_button.style.display = 'flex';
}
