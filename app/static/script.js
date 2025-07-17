$(document).ready(function () {
  $('#add').on('click', function () {
    $('#fields').append('<input type="text" name="name[]" placeholder="Введите имя">');
  });
});
