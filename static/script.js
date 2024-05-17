// SURGE ELEMENT
document.addEventListener("DOMContentLoaded", function() {

    const form = document.getElementById('urlForm');
    form.addEventListener('submit', function(event) {
    });
    document.getElementById('submitButton').addEventListener('click', function() {
      console.log('Button clicked');
      document.getElementById('downloadForm').submit();
    });

});



