document.addEventListener("DOMContentLoaded", main);

let username = "";
let curprof;
function main() {
  $("#profile").hide();
  $("#friends-games-container").hide();
  $('#loading-friends').hide()
}

function loadProfile() {
  username = $("#usrname").val();
  $("#loading").show();
  $('#loading-friends').show()

  // loadFriends()

  $(".profilePrompt").hide("slow");
  fetch("profile/" + username)
    .then((p) => p.json())
    .then(function (profile) {
        curprof=profile;
      $("#profilePicture").attr(
        "src",
        profile.profileUsers[0].settings[0].value
      );
      $("#welcome").text(
        "Welcome " + profile.profileUsers[0].settings[2].value
      );
      $("#profile").show("slow");
      $("#friends-games-container").show();
      profile.games.forEach(function (game) {
        $("#games").append(
          "<div class='game'><img class='gameimg' src='" +
            game.image +
            "'><p>" +
            game.name +
            "</p></div>"
        );
      });
      loadFriends();
      $('#loading-friends').hide()
    })
    .catch(function (error) {
      alert("Invalid Gamertag Try again");
      $(".profilePrompt").show("slow");
    });
}

function loadFriends() {
  fetch("profile/" + username + "/friends")
    .then((p) => p.json())
    .then(function (friends) {
      console.log(friends);
      friendslist = Object.keys(friends).sort();
      console.log(friendslist);
      // First adds users that are online and favorites
      friendslist.forEach((friend) => {
          if(friends[friend].presenceState == 'Online' && friends[friend].isFavorite)
          {
              $(`#friendButtons`).append(`
        <label for="${friend}" class="btn btn-secondary active profile">
          <img src=${
                  friends[friend].displayPicRaw
              } onerror="this.onerror=null; this.src=/Gamerpics/defaultpic.png;"/>
          
          <p>
            <span style='color: ${
                  friends[friend].presenceState == "Online" ? "#68cb58" : "red"
              }'>${friend}*</span>
          </p>
          <input type="checkbox" id="${friend}">
        </label>
         
            `);
          }
      });
      // Then adds users that are online and not favorites
      friendslist.forEach((friend) => {
          if(friends[friend].presenceState == 'Online' && !friends[friend].isFavorite)
          {
              $(`#friendButtons`).append(`
        <label for="${friend}" class="btn btn-secondary active profile">
          <img src=${
                  friends[friend].displayPicRaw
              } onerror="this.onerror=null; this.src=/Gamerpics/defaultpic.png;"/>
          
          <p>
            <span style='color: ${
                  friends[friend].presenceState == "Online" ? "#68cb58" : "red"
              }'>${friend}</span>
          </p>
          <input type="checkbox" id="${friend}">
        </label>
         
            `);
          }
      });
      // Then adds users that are not online and are favorites
      friendslist.forEach((friend) => {
          if(friends[friend].presenceState != 'Online' && friends[friend].isFavorite)
          {
              $(`#friendButtons`).append(`
        <label for="${friend}" class="btn btn-secondary active profile">
          <img src=${
                  friends[friend].displayPicRaw
              } onerror="this.onerror=null; this.src=/Gamerpics/defaultpic.png;"/>
          
          <p>
            <span style='color: ${
                  friends[friend].presenceState == "Online" ? "#68cb58" : "red"
              }'>${friend}*</span>
          </p>
          <input type="checkbox" id="${friend}">
        </label>
         
            `);
          }
      });
      // Then adds users that are not online and are not favorites
      friendslist.forEach((friend) => {
          if(friends[friend].presenceState != 'Online' && !friends[friend].isFavorite)
          {
              $(`#friendButtons`).append(`
        <label for="${friend}" class="btn btn-secondary active profile">
          <img src=${
                  friends[friend].displayPicRaw
              } onerror="this.onerror=null; this.src=/Gamerpics/defaultpic.png;"/>
          
          <p>
            <span style='color: ${
                  friends[friend].presenceState == "Online" ? "#68cb58" : "red"
              }'>${friend}</span>
          </p>
          <input type="checkbox" id="${friend}">
        </label>
         
            `);
          }
      });

      // $('#friends-container').append(`<button type="button" id="more-friends-btn" class="btn btn-primary">Show More</button>`)

      // $('#more-friends-btn').click( () => {
      //   $('#loading').text("All Friends")
      //   $('#more-friends-btn').hide()
      //   friendslist.forEach(friend => {
      //     if(!friends[friend].isFavorite){
      //       $(`#friends`).append(`
      //     <li>
      //       <img src=${friends[friend].displayPicRaw} onerror="this.onerror=null; this.src=/Gamerpics/defaultpic.png;"/>

      //       <p>
      //         <span>${friend}</span>
      //         ${friends[friend].presenceState}
      //       </p>
      //     </li>`
      //     )
      //     }
      //   });
      // });

    })
    .catch(function (error) {
      $("#friends-container").append(
        $("<span> Sorry no friends were found </span>")
      );
    });
}

function games_in_common() {
  // Get all of the selected friends

  // Make post request with body being the list of selected friends

  // display the games in the dom
    let selected=[]

    $('#friendButtons > label > input').each(function (friend){
        if($(this)[0].checked){
            selected.push($(this).attr('id'));
        }
    });

    $("#incommon-list").empty()
    $("#incommon-list").append($("<li class='spinner-border text-success loading' role='status'><span class='sr-only'></span></li>"));

    fetch('profile/friends/incommon',{method :'POST' , body : JSON.stringify(selected)}).then(r=>r.json()).then(function (games){
        if(games['incommon'].length>0){
            games['incommon'].forEach(function (game) {
                $("#incommon-list").append(
                "<li class='game'><img class='gameimg' src='" +
                game.image +
                "'><p>" +
                game.name +
                "</p></li>"
            );
        });
        }

        else{
            $("#incommon-list").append('<li>Sorry no games were found :(</li>');
        }
        $('.loading').remove();


    });




}

function clearElementById(id) {
  let e = document.getElementById(id);
  while (e.firstChild) {
    e.firstChild.remove();
  }
}
