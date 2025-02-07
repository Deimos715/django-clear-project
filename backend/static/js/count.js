(function($) {
  $(document).ready(function() {
    // Функция для создания счетчика символов рядом с полем
    function createCharCount(inputId, label) {
      var charCount = $('<div/>', {
        class: 'char-count',
        id: inputId + '-char-count',
      });

      $('#' + inputId).after(charCount);

      $('#' + inputId).on('input', function() {
        var count = $(this).val().length;
        $('#' + inputId + '-char-count').text(label + ': ' + count + ' символов');
      });

      var initialValue = $('#' + inputId).val();
      if (initialValue) {
        var initialCount = initialValue.length;
        $('#' + inputId + '-char-count').text(label + ': ' + initialCount + ' символов');
      }
    }

    // Создание счетчиков для каждого поля
    createCharCount('id_description', 'Описание');
    createCharCount('id_short_desc', 'Короткое описание');
    createCharCount('id_og_title', 'OG заголовок');
    createCharCount('id_og_description', 'OG описание');
    createCharCount('id_title_page', 'Заголовок страницы');
  });
})(django.jQuery);



