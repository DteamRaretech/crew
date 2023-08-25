{
  const open = document.getElementById('modal-open');
  const container = document.getElementById('modal-container');
  const modalBG = document.getElementById('modal-bg');
  const close = document.getElementById('modal-close');

  open.addEventListener('click', () => {
      container.classList.add('active');
      modalBG.classList.add('active');
  });

  close.addEventListener('click', () => {
      container.classList.remove('active');
      modalBG.classList.remove('active');
  });
  
  modalBG.addEventListener('click', () => {
      container.classList.remove('active');
      modalBG.classList.remove('active');
  });
}