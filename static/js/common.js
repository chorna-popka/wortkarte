var showAlertDialog = function() {
    document
        .getElementById('enter_new_word')
        .show();
    document.querySelector('#deu_wort').focus();
};
var hideAlertDialog = function() {
    document
        .getElementById('enter_new_word')
        .hide();
    document.querySelector('#deu_wort').value = "";
    document.querySelector('#rus_wort').value = "";
};
var goToMenu = function() {
    window.location.replace('/');
}
var addNewWord = function () {
    var deu = document.querySelector('#deu_wort').value;
    var rus = document.querySelector('#rus_wort').value;

    if (deu.length > 1 && rus.length > 1) {
        fetch('/save',
        {
            headers: {
                'Content-Type': 'application/json'
            },
            method: 'POST',
            body: JSON.stringify({
                "deu": deu,
                "rus": rus
            })
        }).then(function (response) { // At this point, Flask has printed our JSON
        return response.text();
        }).then(function (text) {
          if (text == 'OK') {
            hideAlertDialog();
            document.location.reload(true);
          } else if (text == 'NOK') {
                ons.notification.toast('Такое слово уже есть', { timeout: 1000, animation: 'fall' });
          }
        });
    }
};
var getGoogleTranslation = function() {
    var deu = document.querySelector('#deu_wort').value;
    if (deu.length > 1) {
        fetch('/trans',
        {
            // Declare what type of data we're sending
            headers: {
                'Content-Type': 'application/json'
            },
            // Specify the method
            method: 'POST',

            // A JSON payload
            body: JSON.stringify({
                "deu": deu
            })
        }).then(function (response) { // At this point, Flask has printed our JSON
        return response.text();
        }).then(function (text) {
          document.querySelector('#rus_wort').value = text;
      });
    }
}