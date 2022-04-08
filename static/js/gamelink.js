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

  //loadFriends()

  $(".profilePrompt").hide("slow");
  fetch("profile/"+ username)
    .then((p) => p.json())
    .then(function (profile) {
      $("#profilePicture").attr("src", profile.profileUsers[0].settings[0].value);
      $("#welcome").text("Welcome " + profile.profileUsers[0].settings[2].value);
      $("#profile").show("slow");
      $('#friends-container').show();
      profile.games.forEach(function (game){
        $("#games").append("<div class='game'><img class='gameimg' src='" + game.image + "'><span>"+ game.name +"</span></div>");
      });
      loadFriends()
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
      if(friends[friend].isFavorite){
        $(`#friendButtons`).append(`
        <label for="${friend}" class="btn btn-secondary active profile">
          <img src=${friends[friend].displayPicRaw} onerror="this.onerror=null; this.src=/Gamerpics/defaultpic.png;"/>
          
          <p>
            <span>${friend}</span>
            ${friends[friend].presenceState}
          </p>
          <input type="checkbox" id="${friend}">
        </label>
         
       `
      )

      }
    });
    $('#friends-container').append(`<button type="button" id="more-friends-btn" class="btn btn-primary">Show More</button>`)
    
    $('#more-friends-btn').click( () => {
      $('#loading').text("All Friends")
      $('#more-friends-btn').hide()
      friendslist.forEach(friend => {
        if(!friends[friend].isFavorite){
          $(`#friends`).append(`
        <li>
          <img src=${friends[friend].displayPicRaw} onerror="this.onerror=null; this.src=/Gamerpics/defaultpic.png;"/>
          
          <p>
            <span>${friend}</span>
            ${friends[friend].presenceState}
          </p>
        </li>`
        )
        }
      });
    });

    $('#loading').text("Favorite Friends")
  }).catch(function (error){
    $("#loading").hide();
    $("#friends-container").append($("<span> Sorry no friends where found </span>"));
  }

  )
}

function clearElementById(id) {
  let e = document.getElementById(id);
  while(e.firstChild){
      e.firstChild.remove();
  }
}
