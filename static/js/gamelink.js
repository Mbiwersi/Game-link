document.addEventListener("DOMContentLoaded", main);

let username = "";

function main() {
  $("#profile").hide();
  $('#friends-container').hide()
  $('#loading').hide()
}

function loadProfile() {
  username = $("#usrname").val();
  $('#loading').show()

  loadFriends()

  $(".profilePrompt").hide("slow");
  fetch("profile/"+ username)
    .then((p) => p.json())
    .then(function (profile) {
      $("#profilePicture").attr("src", profile.profileUsers[0].settings[0].value);
      $("#welcome").text("Welcome " + profile.profileUsers[0].settings[2].value);
      $("#profile").show("slow");
      $('#friends-container').show();
    })
    .catch(function (error) {
      alert("Invalid Gamertag Try again");
      $(".profilePrompt").show("slow");
    });
}

function loadFriends() {
  fetch("profile/" + username +"/friends")
  .then((p) => p.json())
  .then(function (friends){
    friendslist = Object.keys(friends)
    friendslist.forEach(friend => {
      $(`#friends`).append(`
      <li>
        <img src=${friends[friend].displayPicRaw}/>
        <h1>${friend}</h1>
        <p>${friends[friend].presenceState}</p>
      </li>`
      )
    });
    $('#loading').text("Friends")
  })
}