document.addEventListener("DOMContentLoaded", main);
let username = "";
function main() {
  console.log("HI");
  $("#profile").hide();
}

function loadProfile() {
  username = $("#usrname").val();
  $(".profilePrompt").hide("slow");
  fetch("profile/"+ username)
    .then((p) => p.json())
    .then(function (profile) {
      $("#profilePicture").attr("src", profile.imgurl);
      $("#welcome").text("Welcome " + profile.username);
      $("#profile").show("slow");
    })
    .catch(function (error) {
      alert("Invalid Gamertag Try again");
      $(".profilePrompt").show("slow");
    });
}
