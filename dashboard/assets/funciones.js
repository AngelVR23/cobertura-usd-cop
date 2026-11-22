// Formatos para los recuadros de los deslizadores
window.dccFunctions = window.dccFunctions || {};
window.dccFunctions.formatoUSD = function (valor) {
  return "US$ " + Math.round(valor).toLocaleString("es-CO");
};
window.dccFunctions.formatoPct = function (valor) {
  return String(valor).replace(".", ",") + " %";
};
