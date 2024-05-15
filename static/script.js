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



function populateQualitySelector(selectedType) {
  const qualitySelectorContainer = document.getElementById('qualitySelectorContainer');
  qualitySelectorContainer.innerHTML = ''; // Clear previous options

  // Retrieve the JSON string representing the qualities
  const streamJson = document.getElementById('qualities').value;

  console.log('Qualities JSON:', streamJson); // Debugging: print JSON data to console

  try {
      // Parse the JSON string representing the qualities into a JavaScript array
      const parsedJson = JSON.parse(streamJson);
      const typeQualities = parsedJson[selectedType];
      
      console.log('Parsed qualities:', typeQualities);

      // Populate the quality selector with the available qualities
      typeQualities.forEach(quality => {
          const input = document.createElement('input');
          input.id = quality;
          input.name = quality;
          input.type = 'radio';

          const label = document.createElement('label');
          label.htmlFor = quality;
          label.textContent = quality;

          qualitySelectorContainer.appendChild(input);
          qualitySelectorContainer.appendChild(label);
      });
  } catch (error) {
      console.error('Error parsing JSON data:', error);
  }
}

// Add change event listener to the type selector
document.querySelectorAll('input[name="type"]').forEach(function(radio) {
  radio.addEventListener('change', function() {
      const selectedType = this.value;
      console.log('Selected type:', selectedType);
      populateQualitySelector(selectedType);
  });
});

// Initially populate the quality selector with the qualities of the first MIME type
document.addEventListener('DOMContentLoaded', function() {
  const firstType = document.querySelector('input[name="type"]:checked').value;
  console.log('First type:', firstType);
  populateQualitySelector(firstType);
});