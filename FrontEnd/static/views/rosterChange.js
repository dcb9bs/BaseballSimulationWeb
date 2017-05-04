/**
 * Created by Drew on 5/1/17.
 */
$(document).ready(function() {
    $("#pitcherForm").hide()
    $("#batterForm").hide()

    $("#pitcher_checkbox").change(function(){
        if($("#pitcher_checkbox").is(':checked')){
            $("#pitcherForm").show()
        }else{
            $("#pitcherForm").hide()
        }
    });

    $("#batter_checkbox").change(function(){
        if($("#batter_checkbox").is(':checked')){
            $("#batterForm").show()
        }else{
            $("#batterForm").hide()
        }
    });

    $("#team_select").change(function(){
        var id = $(this).find(":selected").val();
        $.get("/updateTeamSelect/" + id, function(data){
            var i;
            var team = data['batters'];
            $("#batters").empty()
            var append_string = "<table><th>Batters</th>";
            for(i = 0; i < team.length; i++){
                append_string = append_string + "<tr><td value='" + team[i]['id'] + "'>" + team[i]['full_name'] +
                    "</td></tr>";
            }
            append_string = append_string + "</table>";
            $("#batters").append(append_string);
            team = data['pitchers'];
            $("#pitchers").empty();
            var append_string = "<table><th>Pitchers</th>";
            for(i = 0; i < team.length; i++){
                append_string = append_string + "<tr><td value='" + team[i]['id'] + "'>" + team[i]['full_name'] +
                    "</td></tr>";
            }
            append_string = append_string + "</table>";
            $("#pitchers").append(append_string);

        }, "json");
    });




});