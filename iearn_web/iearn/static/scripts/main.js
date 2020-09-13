$(document).ready(function(){
    $(function() {
        var loc = window.location.href; // returns the full URL


        if(/veikla/.test(loc)) {
        $('#veikla_link').addClass('active');         // Header link coloration
        } else if(/projektai/.test(loc) && /visi-projektai/.test(loc) === false) {
            $('#projektai_link').addClass('active');  // Header link coloration
        } else if(/admin/.test(loc)) {
            $('#admin_link').addClass('active');      // Header link coloration

            if(/apie-mus/.test(loc)) {
                $('#about_us_Meniu').addClass('active-list');        //  Admin meniu link coloration
            } else if(/visi-projektai/.test(loc) && /projektai/.test(loc) !== false) {
                $('#all_projects_Meniu').addClass('active-list');   //  Admin meniu link coloration
            } else if(/komandos-nariai/.test(loc)) {
                $('#team_members_Meniu').addClass('active-list');   //  Admin meniu link coloration
            } else if(/mano-info/.test(loc)) {
                $('#my_info_Meniu').addClass('active-list');        //  Admin meniu link coloration
            } else if(/media-kontaktai/.test(loc)) {
                $('#media_contacts_Meniu').addClass('active-list');        //  Admin meniu link coloration
            }
        }
    });
});