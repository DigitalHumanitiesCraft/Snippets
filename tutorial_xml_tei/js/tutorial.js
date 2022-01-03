///////////////////////////////////////////////
// copies text (e.g. from code) into clipboard
function copy(id) {
  ta = document.createElement('textarea');
  ta.value = id.textContent;
  document.body.appendChild(ta);
  ta.select();
  document.execCommand('copy');
  document.body.removeChild(ta);
}