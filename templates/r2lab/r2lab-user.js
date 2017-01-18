{% load jsonify %}
<script type="text/javascript" src="/assets/r2lab/current-slice.js"></script>
<script type="text/javascript">
// globals that describe logged in user 
var r2lab_user = {{r2lab_context.user_details|jsonify|safe}};
// shortcuts
var r2lab_email = {{r2lab_context.user_details.email|jsonify|safe}};
var r2lab_hrn = {{r2lab_context.user_details.hrn|jsonify|safe}};
var r2lab_accounts = {{r2lab_context.accounts|jsonify|safe}};
// initialize current_slice
// javascript code should use 'current_slice.name'
current_slice.init_from_storage(r2lab_accounts);
</script>
