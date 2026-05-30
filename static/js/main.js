// static/js/main.js
$(document).ready(function() {
    // AJAX лайки
    $('.like-btn').click(function() {
        var btn = $(this);
        var poemId = btn.data('poem-id');
        var csrftoken = $('[name=csrfmiddlewaretoken]').val();

        $.ajax({
            url: '/poems/' + poemId + '/like/',
            method: 'POST',
            headers: {'X-CSRFToken': csrftoken},
            dataType: 'json',
            success: function(data) {
                var icon = btn.find('i');
                if (data.liked) {
                    icon.removeClass('far').addClass('fas');
                    btn.addClass('liked');
                } else {
                    icon.removeClass('fas').addClass('far');
                    btn.removeClass('liked');
                }
                btn.find('.likes-count').text(data.likes_count);
            }
        });
    });

    // Анимация при загрузке
    $('.poem-card').each(function(index) {
        $(this).css('animation-delay', (index * 0.1) + 's');
        $(this).addClass('animate__animated animate__fadeInUp');
    });

    // Подтверждение удаления
    $('.delete-confirm').click(function(e) {
        if (!confirm('Вы уверены, что хотите удалить это стихотворение?')) {
            e.preventDefault();
        }
    });
});