var prev = function() {
    var carousel = document.getElementById('carousel');
    carousel.prev();
};

var next = function() {
    var carousel = document.getElementById('carousel');
    carousel.next();
};
var lose = function(a, b) {
    if (a < b) {
        document.querySelector('#wordstack').pushPage('word_' + (a + 1));;
    } else {
        ons.notification.alert('Этот раунд завершен!',{'title':'Готово!'})
        .then(function() {
            window.location.replace('/');
        });

    }
}
var win = function(a, b, c, d) {
    fetch('/mark',
        {
            headers: {
                'Content-Type': 'application/json'
            },
            method: 'POST',
            body: JSON.stringify({
                "id": c,
                "bucket": d
            })
        }).then(function (response) {
            return response.text();
        });
    if (a < b) {
        document.querySelector('#wordstack').pushPage('word_' + (a + 1));;
    } else {
        ons.notification.alert('Этот раунд завершен!',{'title':'Готово!'})
        .then(function() {
            window.location.replace('/');
        });

    }

}
var showEditDialog = function(w_id, source, target) {
    document
        .getElementById('edit_word')
        .show();
    document.querySelector('#source').value = source;
    document.querySelector('#target').value = target;
    document.querySelector('#w_id').value = w_id;
    document.querySelector('#source').focus();
};
var hideEditDialog = function() {
    document
        .getElementById('edit_word')
        .hide();
    document.querySelector('#source').value = "";
    document.querySelector('#target').value = "";
    document.querySelector('#w_id').value = "";
};
var editWord = function() {
    var deu = document.querySelector('#source').value;
    var rus = document.querySelector('#target').value;
    var w_id = document.querySelector('#w_id').value;

    if (deu.length > 1 && rus.length > 1) {
        fetch('/update',
        {
            headers: {
                'Content-Type': 'application/json'
            },
            method: 'POST',
            body: JSON.stringify({
                "deu": deu,
                "rus": rus,
                "w_id": w_id
            })
        }).then(function (response) { // At this point, Flask has printed our JSON
        return response.text();
        }).then(function (text) {
          if (text == 'OK') {
            hideAlertDialog();
            document.location.reload(true);
          } else if (text == 'NOK') {
                ons.notification.toast('Сохранить не удалось', { timeout: 1000, animation: 'fall' });
          }
        });
    }
}
ons.ready(function() {
    if(1==1) {
        document.querySelector('#wordstack').pushPage('word_1');
      } else {
        document.querySelector('#wordstack').pushPage('no_words');
  }
});