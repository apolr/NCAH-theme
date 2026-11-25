<?php
/**
 * Membership join form: [ncah_member_form]
 * Collects WhatsApp Community membership requests. Stored privately for an admin to review
 * (address verification), with an email notice. No data is shown publicly.
 */
if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

const NCAH_CA_AREA_CODES = array( 204, 226, 236, 249, 250, 257, 263, 289, 306, 343, 354, 365, 367, 368, 382, 403, 416, 418, 428, 431, 437, 438, 450, 468, 474, 506, 514, 519, 548, 579, 581, 584, 587, 604, 613, 639, 647, 672, 683, 705, 709, 742, 753, 778, 780, 782, 807, 819, 825, 867, 873, 879, 902, 905, 942 );

add_action( 'init', function () {
	register_post_type( 'ncah_member', array(
		'labels'          => array( 'name' => 'Member applications', 'singular_name' => 'Member application', 'menu_name' => 'Member applications' ),
		'public'          => false,
		'show_ui'         => true,
		'show_in_menu'    => true,
		'menu_icon'       => 'dashicons-groups',
		'menu_position'   => 26,
		'supports'        => array( 'title' ),
		'capability_type' => 'post',
		'capabilities'    => array( 'create_posts' => 'do_not_allow' ),
		'map_meta_cap'    => true,
	) );
} );

function ncah_member_fields() {
	return array( 'whatsapp' => 'WhatsApp number', 'address' => 'Address', 'referral' => 'Referral name', 'donor' => 'Also a donor', 'frequency' => 'Donation frequency', 'verified' => 'Address verified', 'consent' => 'Consent given' );
}

add_filter( 'manage_ncah_member_posts_columns', function () {
	return array( 'cb' => '<input type="checkbox" />', 'title' => 'Full name', 'whatsapp' => 'WhatsApp', 'address' => 'Address', 'referral' => 'Referral', 'donor' => 'Donor / frequency', 'verified' => 'Address verified', 'date' => 'Submitted' );
} );
add_action( 'manage_ncah_member_posts_custom_column', function ( $col, $id ) {
	if ( 'donor' === $col ) {
		echo esc_html( get_post_meta( $id, 'donor', true ) === 'yes' ? 'Yes: ' . get_post_meta( $id, 'frequency', true ) : 'No' );
	} elseif ( 'verified' === $col ) {
		$v = get_post_meta( $id, 'verified', true ) === 'yes';
		echo $v ? '<strong style="color:#008000">Verified</strong>' : '<span style="color:#b32d2e">Pending</span>';
	} elseif ( in_array( $col, array( 'whatsapp', 'address', 'referral' ), true ) ) {
		echo esc_html( get_post_meta( $id, $col, true ) );
	}
}, 10, 2 );

add_filter( 'post_row_actions', function ( $actions, $post ) {
	if ( 'ncah_member' === $post->post_type && current_user_can( 'edit_post', $post->ID ) ) {
		$v   = get_post_meta( $post->ID, 'verified', true ) === 'yes';
		$url = wp_nonce_url( admin_url( 'admin-post.php?action=ncah_member_verify&id=' . $post->ID . '&set=' . ( $v ? 'no' : 'yes' ) ), 'ncah_verify_' . $post->ID );
		$actions['ncah_verify'] = '<a href="' . esc_url( $url ) . '">' . ( $v ? 'Mark address unverified' : 'Mark address verified' ) . '</a>';
		unset( $actions['inline hide-if-no-js'] );
	}
	return $actions;
}, 10, 2 );

add_action( 'admin_post_ncah_member_verify', function () {
	$id = absint( $_GET['id'] ?? 0 );
	check_admin_referer( 'ncah_verify_' . $id );
	if ( $id && current_user_can( 'edit_post', $id ) && 'ncah_member' === get_post_type( $id ) ) {
		update_post_meta( $id, 'verified', 'yes' === ( $_GET['set'] ?? '' ) ? 'yes' : 'no' );
	}
	wp_safe_redirect( admin_url( 'edit.php?post_type=ncah_member' ) );
	exit;
} );

add_action( 'add_meta_boxes', function () {
	add_meta_box( 'ncah_member_details', 'Application details', function ( $post ) {
		echo '<table class="form-table"><tbody>';
		foreach ( ncah_member_fields() as $k => $label ) {
			echo '<tr><th>' . esc_html( $label ) . '</th><td>' . esc_html( (string) get_post_meta( $post->ID, $k, true ) ) . '</td></tr>';
		}
		echo '</tbody></table>';
	}, 'ncah_member', 'normal', 'high' );
} );

function ncah_member_normalise_phone( $raw ) {
	$d = preg_replace( '/\D+/', '', (string) $raw );
	if ( 11 === strlen( $d ) && '1' === $d[0] ) {
		$d = substr( $d, 1 );
	}
	if ( 10 !== strlen( $d ) || ! in_array( (int) substr( $d, 0, 3 ), NCAH_CA_AREA_CODES, true ) ) {
		return false;
	}
	return '+1 (' . substr( $d, 0, 3 ) . ') ' . substr( $d, 3, 3 ) . '-' . substr( $d, 6 );
}

function ncah_member_provinces() {
	return array( 'ON' => 'Ontario', 'AB' => 'Alberta', 'BC' => 'British Columbia', 'MB' => 'Manitoba', 'NB' => 'New Brunswick', 'NL' => 'Newfoundland and Labrador', 'NS' => 'Nova Scotia', 'NT' => 'Northwest Territories', 'NU' => 'Nunavut', 'PE' => 'Prince Edward Island', 'QC' => 'Quebec', 'SK' => 'Saskatchewan', 'YT' => 'Yukon' );
}

add_shortcode( 'ncah_member_form', function () {
	$status = sanitize_key( $_GET['ncah_join'] ?? '' );
	if ( 'ok' === $status ) {
		return '<div class="ncah-form-note ncah-form-note--ok" role="status"><h3>Thank you, your request has been received.</h3><p>An administrator will verify your address and then send you the invitation to the NCAH WhatsApp Community.</p></div>';
	}
	$err = array(
		'phone'   => 'Please enter a Canadian WhatsApp number, for example 289 244 2568.',
		'postal'  => 'Please enter a valid Canadian postal code, for example L8P 1A1.',
		'missing' => 'Please complete all required fields.',
		'freq'    => 'Please choose how often you would like to give.',
		'spam'    => 'We could not submit your request. Please try again.',
		'wait'    => 'Too many requests from this connection. Please try again later.',
	);
	$msg = $err[ $status ] ?? '';
	ob_start();
	?>
	<form class="ncah-form" method="post" action="<?php echo esc_url( admin_url( 'admin-post.php' ) ); ?>" novalidate>
		<?php if ( $msg ) : ?><div class="ncah-form-note ncah-form-note--err" role="alert"><?php echo esc_html( $msg ); ?></div><?php endif; ?>
		<input type="hidden" name="action" value="ncah_member_apply">
		<?php wp_nonce_field( 'ncah_member_apply', 'ncah_nonce' ); ?>
		<input type="hidden" name="ncah_t" value="<?php echo esc_attr( time() ); ?>">
		<p class="ncah-hp" aria-hidden="true"><label>Leave this empty <input type="text" name="ncah_site" tabindex="-1" autocomplete="off"></label></p>

		<p><label for="ncah-name">Full name <span aria-hidden="true">*</span></label>
			<input id="ncah-name" name="full_name" type="text" autocomplete="name" required></p>

		<p><label for="ncah-wa">WhatsApp number (Canadian line) <span aria-hidden="true">*</span></label>
			<input id="ncah-wa" name="whatsapp" type="tel" inputmode="tel" autocomplete="tel" placeholder="289 244 2568" required>
			<small>Must be a Canadian number. This is the number we will invite to the WhatsApp Community.</small></p>

		<fieldset>
			<legend>Address <span aria-hidden="true">*</span></legend>
			<p><label for="ncah-street">Street address</label><input id="ncah-street" name="street" type="text" autocomplete="address-line1" required></p>
			<div class="ncah-form-row">
				<p><label for="ncah-city">City</label><input id="ncah-city" name="city" type="text" autocomplete="address-level2" required></p>
				<p><label for="ncah-prov">Province</label>
					<input id="ncah-prov" type="text" value="Ontario" readonly aria-readonly="true" autocomplete="address-level1">
					<input type="hidden" name="province" value="ON"></p>
				<p><label for="ncah-postal">Postal code</label><input id="ncah-postal" name="postal" type="text" autocomplete="postal-code" placeholder="L8P 1A1" required></p>
			</div>
			<small>An administrator verifies every address before the invitation is sent.</small>
		</fieldset>

		<p><label for="ncah-ref">Referral name <span class="ncah-opt">(optional)</span></label>
			<input id="ncah-ref" name="referral" type="text">
			<small>The name of the member or person who referred you.</small></p>

		<p class="ncah-check"><label><input type="checkbox" name="donor" value="yes" id="ncah-donor"> I would also like to be a donor to the cause of the Association.</label></p>

		<fieldset id="ncah-freq" class="ncah-freq" hidden>
			<legend>How often would you like to give?</legend>
			<?php foreach ( array( 'Monthly', 'Quarterly', 'Bi-annually', 'Annually' ) as $f ) : ?>
				<label class="ncah-radio"><input type="radio" name="frequency" value="<?php echo esc_attr( $f ); ?>"> <?php echo esc_html( $f ); ?></label>
			<?php endforeach; ?>
			<small>Donating is optional and does not affect your membership.</small>
		</fieldset>

		<p class="ncah-check"><label><input type="checkbox" name="consent" value="yes" required> I agree that NCAH may store these details to process my membership, as described in the <a href="<?php echo esc_url( home_url( '/privacy-policy/' ) ); ?>">Privacy Policy</a>. <span aria-hidden="true">*</span></label></p>

		<p><button type="submit" class="wp-block-button__link wp-element-button has-white-color has-ncah-red-background-color has-text-color has-background">Request to join</button></p>
	</form>
	<script>
	( function () {
		var box = document.getElementById( 'ncah-donor' ), grp = document.getElementById( 'ncah-freq' );
		if ( ! box || ! grp ) { return; }
		function sync() { grp.hidden = ! box.checked; grp.querySelectorAll( 'input' ).forEach( function ( r ) { r.required = box.checked && r.type === 'radio' && r.value === 'Monthly'; } ); }
		box.addEventListener( 'change', sync ); sync();
	} )();
	</script>
	<?php
	return ob_get_clean();
} );

function ncah_member_redirect( $code ) {
	$back = wp_get_referer() ?: home_url( '/membership/' );
	wp_safe_redirect( add_query_arg( 'ncah_join', $code, remove_query_arg( 'ncah_join', $back ) ) . ( 'ok' === $code ? '' : '#join' ) );
	exit;
}

function ncah_member_handle() {
	if ( ! isset( $_POST['ncah_nonce'] ) || ! wp_verify_nonce( sanitize_text_field( wp_unslash( $_POST['ncah_nonce'] ) ), 'ncah_member_apply' ) ) {
		ncah_member_redirect( 'spam' );
	}
	if ( ! empty( $_POST['ncah_site'] ) || ( time() - (int) ( $_POST['ncah_t'] ?? 0 ) ) < 4 ) {
		ncah_member_redirect( 'spam' );
	}
	$ip  = 'ncah_join_' . md5( (string) ( $_SERVER['REMOTE_ADDR'] ?? '' ) );
	$hit = (int) get_transient( $ip );
	if ( $hit >= 5 ) {
		ncah_member_redirect( 'wait' );
	}
	$g = function ( $k ) { return sanitize_text_field( wp_unslash( $_POST[ $k ] ?? '' ) ); };
	$name = $g( 'full_name' ); $street = $g( 'street' ); $city = $g( 'city' ); $prov = 'ON'; $postal = strtoupper( $g( 'postal' ) ); $ref = $g( 'referral' );
	if ( '' === $name || '' === $street || '' === $city || empty( $_POST['consent'] ) || ! isset( ncah_member_provinces()[ $prov ] ) ) {
		ncah_member_redirect( 'missing' );
	}
	$phone = ncah_member_normalise_phone( $g( 'whatsapp' ) );
	if ( ! $phone ) {
		ncah_member_redirect( 'phone' );
	}
	if ( ! preg_match( '/^[ABCEGHJ-NPRSTVXY]\d[ABCEGHJ-NPRSTV-Z][ -]?\d[ABCEGHJ-NPRSTV-Z]\d$/', $postal ) ) {
		ncah_member_redirect( 'postal' );
	}
	$postal = substr( $postal, 0, 3 ) . ' ' . substr( preg_replace( '/[ -]/', '', $postal ), 3 );
	$donor  = ( 'yes' === ( $_POST['donor'] ?? '' ) ) ? 'yes' : 'no';
	$freq   = $g( 'frequency' );
	if ( 'yes' === $donor && ! in_array( $freq, array( 'Monthly', 'Quarterly', 'Bi-annually', 'Annually' ), true ) ) {
		ncah_member_redirect( 'freq' );
	}
	if ( 'no' === $donor ) {
		$freq = '';
	}
	set_transient( $ip, $hit + 1, HOUR_IN_SECONDS );
	$id = wp_insert_post( array( 'post_type' => 'ncah_member', 'post_status' => 'publish', 'post_title' => $name ) );
	if ( ! $id || is_wp_error( $id ) ) {
		ncah_member_redirect( 'spam' );
	}
	$address = $street . ', ' . $city . ', ' . $prov . ' ' . $postal;
	foreach ( array( 'whatsapp' => $phone, 'address' => $address, 'referral' => $ref, 'donor' => $donor, 'frequency' => $freq, 'verified' => 'no', 'consent' => 'yes ' . gmdate( 'Y-m-d H:i' ) . ' UTC' ) as $k => $v ) {
		update_post_meta( $id, $k, $v );
	}
	$to   = get_option( 'ncah_member_notify', 'info@ncahamilton.ca' );
	$body = "New membership request\n\nName: $name\nWhatsApp: $phone\nAddress (to verify): $address\nReferral: $ref\nDonor: $donor" . ( $freq ? " ($freq)" : '' ) . "\n\nReview: " . admin_url( 'edit.php?post_type=ncah_member' );
	wp_mail( $to, 'New NCAH membership request: ' . $name, $body );
	ncah_member_redirect( 'ok' );
}
add_action( 'admin_post_nopriv_ncah_member_apply', 'ncah_member_handle' );
add_action( 'admin_post_ncah_member_apply', 'ncah_member_handle' );
