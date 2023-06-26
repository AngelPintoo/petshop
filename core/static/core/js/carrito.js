function calcularTotal(cantidad, precio, productoId) {
    var total = cantidad * precio;
    $('.total-' + productoId).text(total.toFixed(2));

    // Actualizar el valor del total en la página de pago
    var nuevoTotal = 0;
    $('.total').each(function() {
        nuevoTotal += parseFloat($(this).text());
    });
    $('#totalPagar').text('$' + nuevoTotal.toFixed(2));
}

$(document).ready(function() {
    $('.quantity').on('change', function() {
        var cantidad = parseInt($(this).val());
        var precio = parseFloat($(this).closest('tr').find('.price').text());
        var productoId = $(this).data('producto-id');
        calcularTotal(cantidad, precio, productoId);
    });

    calcularTotal(); // Calcular el total inicial al cargar la página
});