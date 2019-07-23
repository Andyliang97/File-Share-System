document.querySelector(".upload-button").addEventListener("click", function() {
  console.log('clicked')
  document.getElementById("upload-input").click();
});

document.getElementById("upload-input").onchange = function() {
    document.querySelector(".upload-form").submit();
};