/**
 * Created by Drew on 5/1/17.
 */
$(document).ready(function() {
    var pitcher = $("#pitcherForm");
    var batter = $("#batterForm");
    pitcher.hide()
    $("#pitcherForm input").attr("required", false);
    batter.hide()
    $("#batterForm input").attr("required", false);

    $("#pitcher_checkbox").change(function(){
        if($("#pitcher_checkbox").is(':checked')){
            pitcher.show()
            $("#pitcherForm input").attr("required", true);

        }else{
            pitcher.hide()
            $("#pitcherForm input").attr("required", false);
        }
    });

    $("#batter_checkbox").change(function(){
        if($("#batter_checkbox").is(':checked')){
            batter.show()
            $("#batterForm input").attr("required", true);
        }else{
            batter.hide()
            $("#batterForm input").attr("required", false);
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