var input = document.querySelector('#file-input');
input.addEventListener('change',preview);
function preview() {
    var fileObject = this. files[0]; 
    var fileReader = new FileReader();
         fileReader.readAsDataURL(fileobject);
    fileReader.onload = function () {
         var result = fileReader.result; 
         var img =document.querySelector('') 
    }
}