$(document).ready(function() {
    $('#kraken-api').on('input', function() {
        $('#kraken-update').addClass("is-visible");
    });
    $('#kraken-secret').on('input', function() {
        $('#kraken-update').addClass("is-visible");
    });
    $('#cryptocom-api').on('input', function() {
        $('#cryptocom-update').addClass("is-visible");
    });
    $('#cryptocom-secret').on('input', function() {
        $('#cryptocom-update').addClass("is-visible");
    });
});