<?php
/**
 * Business directory.
 *  [ncah_business_directory]  public list of approved member businesses
 *  [ncah_business_form]       listing request form (members only)
 *
 * Each listing has a directory status set by an admin: pending, approved, suspended or blacklisted.
 * Only "approved" listings are public. A blacklisted business or email cannot send a new request.
 */
if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

function ncah_dir_statuses() {
	return array(
		'pending'     => 'Pending review',
		'approved'    => 'Approved',
		'suspended'   => 'Suspended',
		'blacklisted' => 'Blacklisted',
	);
}

function ncah_dir_reg_options() {
	return array(
		'ontario' => 'Registered in Ontario',
		'canada'  => 'Registered in Canada, another province or federally',
		'no'      => 'Not registered yet',
	);
}

function ncah_dir_fields() {
	return array(
		'reg_status'     => 'Business registration',
		'description'    => 'Service or product description',
		'address'        => 'Address',
		'contact_person' => 'Contact person',
		'phone'          => 'Phone',
		'whatsapp'       => 'WhatsApp number',
		'email'          => 'Email',
		'website'        => 'Website',
	);
}

add_action( 'init', function () {
	register_post_type( 'ncah_business', array(
		'labels'          => array(
			'name'          => 'Business directory',
			'singular_name' => 'Business',
			'menu_name'     => 'Business directory',
			'add_new_item'  => 'Add business',
			'edit_item'     => 'Edit business',
			'all_items'     => 'All businesses',
			'search_items'  => 'Search businesses',
		),
		'public'          => false,
		'show_ui'         => true,
		'show_in_menu'    => true,
		'menu_icon'       => 'dashicons-store',
		'menu_position'   => 27,
		'supports'        => array( 'title' ),
		'capability_type' => 'post',
		'map_meta_cap'    => true,
	) );
	register_taxonomy( 'business_category', 'ncah_business', array(
		'labels'            => array( 'name' => 'Business categories', 'singular_name' => 'Business category', 'menu_name' => 'Categories' ),
		'public'            => false,
		'show_ui'           => true,
		'hierarchical'      => true,
		'show_admin_column' => true,
		'rewrite'           => false,
	) );
	// Starter categories, created once. Admins can rename, add or remove them under Business directory > Categories.
	if ( ! get_option( 'ncah_dir_seeded' ) ) {
		foreach ( array( 'Food and catering', 'Retail and fashion', 'Beauty and wellness', 'Professional services', 'Finance and insurance', 'Real estate', 'Health and care', 'Education and tutoring', 'Transport and logistics', 'Technology', 'Events and entertainment', 'Trades and construction', 'Other' ) as $t ) {
			if ( ! term_exists( $t, 'business_category' ) ) {
				wp_insert_term( $t, 'business_category' );
			}
		}
		update_option( 'ncah_dir_seeded', 1 );
	}
} );

/* ---------------------------------------------------------------- Admin: columns, filters, actions */

add_filter( 'manage_ncah_business_posts_columns', function () {
	return array(
		'cb'              => '<input type="checkbox" />',
		'title'           => 'Business',
		'taxonomy-business_category' => 'Category',
		'ncah_contact'    => 'Contact',
		'ncah_reg'        => 'Registration',
		'ncah_dstatus'    => 'Directory status',
		'date'            => 'Submitted',
	);
} );

add_action( 'manage_ncah_business_posts_custom_column', function ( $col, $id ) {
	if ( 'ncah_contact' === $col ) {
		echo esc_html( get_post_meta( $id, 'contact_person', true ) ) . '<br>' . esc_html( get_post_meta( $id, 'phone', true ) ) . '<br>' . esc_html( get_post_meta( $id, 'email', true ) );
	} elseif ( 'ncah_reg' === $col ) {
		$r = get_post_meta( $id, 'reg_status', true );
		echo esc_html( ncah_dir_reg_options()[ $r ] ?? '' );
	} elseif ( 'ncah_dstatus' === $col ) {
		$s      = get_post_meta( $id, 'directory_status', true ) ?: 'pending';
		$colors = array( 'pending' => '#996800', 'approved' => '#008000', 'suspended' => '#b32d2e', 'blacklisted' => '#1d2327' );
		echo '<strong style="color:' . esc_attr( $colors[ $s ] ?? '#1d2327' ) . '">' . esc_html( ncah_dir_statuses()[ $s ] ?? $s ) . '</strong>';
	}
}, 10, 2 );

add_filter( 'post_row_actions', function ( $actions, $post ) {
	if ( 'ncah_business' !== $post->post_type || ! current_user_can( 'edit_post', $post->ID ) ) {
		return $actions;
	}
	unset( $actions['inline hide-if-no-js'] );
	$s    = get_post_meta( $post->ID, 'directory_status', true ) ?: 'pending';
	$link = function ( $set, $label ) use ( $post ) {
		$url = wp_nonce_url( admin_url( 'admin-post.php?action=ncah_biz_status&id=' . $post->ID . '&set=' . $set ), 'ncah_biz_' . $post->ID );
		return '<a href="' . esc_url( $url ) . '">' . esc_html( $label ) . '</a>';
	};
	if ( 'approved' !== $s ) {
		$actions['ncah_approve'] = $link( 'approved', in_array( $s, array( 'suspended', 'blacklisted' ), true ) ? 'Reinstate' : 'Approve' );
	}
	if ( 'approved' === $s ) {
		$actions['ncah_suspend'] = $link( 'suspended', 'Suspend' );
	}
	if ( 'blacklisted' !== $s ) {
		$actions['ncah_blacklist'] = $link( 'blacklisted', 'Blacklist' );
	}
	return $actions;
}, 10, 2 );

add_action( 'admin_post_ncah_biz_status', function () {
	$id  = absint( $_GET['id'] ?? 0 );
	$set = sanitize_key( $_GET['set'] ?? '' );
	check_admin_referer( 'ncah_biz_' . $id );
	if ( $id && current_user_can( 'edit_post', $id ) && 'ncah_business' === get_post_type( $id ) && isset( ncah_dir_statuses()[ $set ] ) ) {
		update_post_meta( $id, 'directory_status', $set );
		update_post_meta( $id, 'directory_status_changed', gmdate( 'Y-m-d H:i' ) . ' UTC by ' . wp_get_current_user()->user_login );
	}
	wp_safe_redirect( wp_get_referer() ?: admin_url( 'edit.php?post_type=ncah_business' ) );
	exit;
} );

// Status filter links above the list.
add_filter( 'views_edit-ncah_business', function ( $views ) {
	$cur = sanitize_key( $_GET['dir_status'] ?? '' );
	foreach ( ncah_dir_statuses() as $k => $label ) {
		$q = new WP_Query( array( 'post_type' => 'ncah_business', 'post_status' => 'any', 'fields' => 'ids', 'posts_per_page' => 1, 'meta_query' => ncah_dir_status_query( $k ), 'no_found_rows' => false ) );
		$views[ 'dir_' . $k ] = '<a href="' . esc_url( admin_url( 'edit.php?post_type=ncah_business&dir_status=' . $k ) ) . '"' . ( $cur === $k ? ' class="current"' : '' ) . '>' . esc_html( $label ) . ' <span class="count">(' . (int) $q->found_posts . ')</span></a>';
	}
	return $views;
} );

function ncah_dir_status_query( $status ) {
	if ( 'pending' === $status ) {
		return array( 'relation' => 'OR', array( 'key' => 'directory_status', 'value' => 'pending' ), array( 'key' => 'directory_status', 'compare' => 'NOT EXISTS' ) );
	}
	return array( array( 'key' => 'directory_status', 'value' => $status ) );
}

add_action( 'pre_get_posts', function ( $q ) {
	if ( is_admin() && $q->is_main_query() && 'ncah_business' === $q->get( 'post_type' ) && ! empty( $_GET['dir_status'] ) ) {
		$s = sanitize_key( $_GET['dir_status'] );
		if ( isset( ncah_dir_statuses()[ $s ] ) ) {
			$q->set( 'meta_query', ncah_dir_status_query( $s ) );
		}
	}
} );

/* ---------------------------------------------------------------- Admin: edit screen */

add_action( 'add_meta_boxes', function () {
	add_meta_box( 'ncah_biz_status', 'Directory status', function ( $post ) {
		wp_nonce_field( 'ncah_biz_save', 'ncah_biz_nonce' );
		$cur = get_post_meta( $post->ID, 'directory_status', true );
		if ( '' === $cur ) {
			$cur = ( 'auto-draft' === $post->post_status ) ? 'approved' : 'pending';
		}
		echo '<p><select name="directory_status" style="width:100%">';
		foreach ( ncah_dir_statuses() as $k => $label ) {
			echo '<option value="' . esc_attr( $k ) . '"' . selected( $cur, $k, false ) . '>' . esc_html( $label ) . '</option>';
		}
		echo '</select></p>';
		echo '<p class="description">Only <strong>Approved</strong> businesses appear on the public directory. Suspended and blacklisted businesses are hidden. A blacklisted business name or email cannot send a new request.</p>';
		echo '<p><label for="directory_note"><strong>Internal note</strong></label><textarea id="directory_note" name="directory_note" rows="3" style="width:100%">' . esc_textarea( (string) get_post_meta( $post->ID, 'directory_note', true ) ) . '</textarea></p>';
		$ch = get_post_meta( $post->ID, 'directory_status_changed', true );
		if ( $ch ) {
			echo '<p class="description">Last status change: ' . esc_html( $ch ) . '</p>';
		}
	}, 'ncah_business', 'side', 'high' );

	add_meta_box( 'ncah_biz_details', 'Business details', function ( $post ) {
		echo '<table class="form-table"><tbody>';
		$reg = get_post_meta( $post->ID, 'reg_status', true );
		echo '<tr><th><label for="reg_status">Business registration</label></th><td><select id="reg_status" name="reg_status"><option value="">Select</option>';
		foreach ( ncah_dir_reg_options() as $k => $l ) {
			echo '<option value="' . esc_attr( $k ) . '"' . selected( $reg, $k, false ) . '>' . esc_html( $l ) . '</option>';
		}
		echo '</select></td></tr>';
		echo '<tr><th><label for="description">Service or product description</label></th><td><textarea id="description" name="description" rows="5" class="large-text">' . esc_textarea( (string) get_post_meta( $post->ID, 'description', true ) ) . '</textarea></td></tr>';
		foreach ( array( 'address' => 'Address', 'contact_person' => 'Contact person', 'phone' => 'Phone', 'whatsapp' => 'WhatsApp number', 'email' => 'Email', 'website' => 'Website' ) as $k => $label ) {
			echo '<tr><th><label for="' . esc_attr( $k ) . '">' . esc_html( $label ) . '</label></th><td><input type="text" class="large-text" id="' . esc_attr( $k ) . '" name="' . esc_attr( $k ) . '" value="' . esc_attr( (string) get_post_meta( $post->ID, $k, true ) ) . '"></td></tr>';
		}
		$consent = get_post_meta( $post->ID, 'consent', true );
		if ( $consent ) {
			echo '<tr><th>Consent to public listing</th><td>' . esc_html( $consent ) . '</td></tr>';
		}
		echo '</tbody></table>';
	}, 'ncah_business', 'normal', 'high' );
} );

add_action( 'save_post_ncah_business', function ( $id ) {
	if ( ! isset( $_POST['ncah_biz_nonce'] ) || ! wp_verify_nonce( sanitize_text_field( wp_unslash( $_POST['ncah_biz_nonce'] ) ), 'ncah_biz_save' ) || ! current_user_can( 'edit_post', $id ) || ( defined( 'DOING_AUTOSAVE' ) && DOING_AUTOSAVE ) ) {
		return;
	}
	foreach ( array( 'address', 'contact_person', 'phone', 'whatsapp', 'email' ) as $k ) {
		update_post_meta( $id, $k, sanitize_text_field( wp_unslash( $_POST[ $k ] ?? '' ) ) );
	}
	update_post_meta( $id, 'website', esc_url_raw( wp_unslash( $_POST['website'] ?? '' ) ) );
	update_post_meta( $id, 'description', sanitize_textarea_field( wp_unslash( $_POST['description'] ?? '' ) ) );
	update_post_meta( $id, 'directory_note', sanitize_textarea_field( wp_unslash( $_POST['directory_note'] ?? '' ) ) );
	$reg = sanitize_key( $_POST['reg_status'] ?? '' );
	update_post_meta( $id, 'reg_status', isset( ncah_dir_reg_options()[ $reg ] ) ? $reg : '' );
	$new = sanitize_key( $_POST['directory_status'] ?? 'pending' );
	if ( isset( ncah_dir_statuses()[ $new ] ) && get_post_meta( $id, 'directory_status', true ) !== $new ) {
		update_post_meta( $id, 'directory_status', $new );
		update_post_meta( $id, 'directory_status_changed', gmdate( 'Y-m-d H:i' ) . ' UTC by ' . wp_get_current_user()->user_login );
	}
} );

/* ---------------------------------------------------------------- Public list */

function ncah_dir_wa_link( $raw ) {
	$d = preg_replace( '/\D+/', '', (string) $raw );
	return $d ? 'https://wa.me/' . ( 10 === strlen( $d ) ? '1' . $d : $d ) : '';
}

add_shortcode( 'ncah_business_directory', function () {
	$q = new WP_Query( array(
		'post_type'      => 'ncah_business',
		'post_status'    => 'publish',
		'posts_per_page' => -1,
		'orderby'        => 'title',
		'order'          => 'ASC',
		'meta_query'     => array( array( 'key' => 'directory_status', 'value' => 'approved' ) ),
	) );
	if ( ! $q->have_posts() ) {
		return '<div class="ncah-dir-empty"><p>No businesses are listed yet. Members can request a listing using the form below.</p></div>';
	}
	$cats = array();
	ob_start();
	$cards = '';
	foreach ( $q->posts as $p ) {
		$terms  = wp_get_post_terms( $p->ID, 'business_category' );
		$cat    = $terms && ! is_wp_error( $terms ) ? $terms[0]->name : '';
		if ( $cat ) {
			$cats[ $cat ] = true;
		}
		$m      = function ( $k ) use ( $p ) { return (string) get_post_meta( $p->ID, $k, true ); };
		$web    = $m( 'website' );
		$wa     = ncah_dir_wa_link( $m( 'whatsapp' ) );
		$search = strtolower( $p->post_title . ' ' . $cat . ' ' . $m( 'description' ) . ' ' . $m( 'address' ) );
		$cards .= '<article class="ncah-biz" data-cat="' . esc_attr( $cat ) . '" data-search="' . esc_attr( $search ) . '">';
		if ( $cat ) {
			$cards .= '<span class="ncah-biz__cat">' . esc_html( $cat ) . '</span>';
		}
		$cards .= '<h3>' . esc_html( $p->post_title ) . '</h3>';
		$cards .= '<p class="ncah-biz__desc">' . esc_html( $m( 'description' ) ) . '</p><ul class="ncah-biz__meta">';
		if ( $m( 'address' ) ) {
			$cards .= '<li><span>Address</span> ' . esc_html( $m( 'address' ) ) . '</li>';
		}
		if ( $m( 'contact_person' ) ) {
			$cards .= '<li><span>Contact</span> ' . esc_html( $m( 'contact_person' ) ) . '</li>';
		}
		if ( $m( 'phone' ) ) {
			$cards .= '<li><span>Phone</span> <a href="tel:' . esc_attr( preg_replace( '/[^\d+]/', '', $m( 'phone' ) ) ) . '">' . esc_html( $m( 'phone' ) ) . '</a></li>';
		}
		if ( $m( 'email' ) ) {
			$cards .= '<li><span>Email</span> <a href="mailto:' . esc_attr( $m( 'email' ) ) . '">' . esc_html( $m( 'email' ) ) . '</a></li>';
		}
		$cards .= '</ul><p class="ncah-biz__links">';
		if ( $wa ) {
			$cards .= '<a class="ncah-biz__btn" href="' . esc_url( $wa ) . '" target="_blank" rel="noopener">WhatsApp</a>';
		}
		if ( $web ) {
			$cards .= '<a class="ncah-biz__btn ncah-biz__btn--ghost" href="' . esc_url( $web ) . '" target="_blank" rel="noopener">Website</a>';
		}
		$cards .= '</p></article>';
	}
	ksort( $cats );
	?>
	<div class="ncah-dir" id="ncah-dir">
		<div class="ncah-dir__tools">
			<label class="screen-reader-text" for="ncah-dir-q">Search the directory</label>
			<input id="ncah-dir-q" type="search" placeholder="Search by name, service or area">
			<label class="screen-reader-text" for="ncah-dir-cat">Filter by category</label>
			<select id="ncah-dir-cat"><option value="">All categories</option>
				<?php foreach ( array_keys( $cats ) as $c ) : ?><option value="<?php echo esc_attr( $c ); ?>"><?php echo esc_html( $c ); ?></option><?php endforeach; ?>
			</select>
		</div>
		<div class="ncah-dir__grid"><?php echo $cards; // phpcs:ignore WordPress.Security.EscapeOutput -- escaped above ?></div>
		<p class="ncah-dir__none" hidden>No businesses match your search.</p>
	</div>
	<script>
	( function () {
		var root = document.getElementById( 'ncah-dir' ); if ( ! root ) { return; }
		var q = root.querySelector( '#ncah-dir-q' ), c = root.querySelector( '#ncah-dir-cat' ), cards = root.querySelectorAll( '.ncah-biz' ), none = root.querySelector( '.ncah-dir__none' );
		function run() {
			var t = q.value.trim().toLowerCase(), k = c.value, n = 0;
			cards.forEach( function ( el ) {
				var ok = ( ! k || el.dataset.cat === k ) && ( ! t || el.dataset.search.indexOf( t ) > -1 );
				el.hidden = ! ok; if ( ok ) { n++; }
			} );
			none.hidden = n > 0;
		}
		q.addEventListener( 'input', run ); c.addEventListener( 'change', run );
	} )();
	</script>
	<?php
	return ob_get_clean();
} );

/* ---------------------------------------------------------------- Request form */

add_shortcode( 'ncah_business_form', function () {
	$status = sanitize_key( $_GET['ncah_biz'] ?? '' );
	if ( 'ok' === $status ) {
		return '<div class="ncah-form-note ncah-form-note--ok" role="status"><h3>Thank you, your request has been received.</h3><p>An administrator will verify your membership and business details. Once approved, your business will appear in the directory. We have sent a confirmation to your email.</p></div>';
	}
	$err = array(
		'member'  => 'Only registered NCAH members can list a business. Please register as a member first, then submit this form.',
		'phone'   => 'Please enter a Canadian phone number, for example 289 244 2568.',
		'wa'      => 'Please enter the WhatsApp number as a Canadian number, for example 289 244 2568, or leave it empty.',
		'email'   => 'Please enter a valid email address.',
		'postal'  => 'Please enter a valid Canadian postal code, for example L8P 1A1.',
		'missing' => 'Please complete all required fields.',
		'spam'    => 'We could not submit your request. Please try again.',
		'wait'    => 'Too many requests from this connection. Please try again later.',
	);
	$msg   = $err[ $status ] ?? '';
	$terms = get_terms( array( 'taxonomy' => 'business_category', 'hide_empty' => false ) );
	$join  = home_url( '/membership/#join' );
	ob_start();
	?>
	<form class="ncah-form ncah-bizform" method="post" action="<?php echo esc_url( admin_url( 'admin-post.php' ) ); ?>" novalidate>
		<?php if ( $msg ) : ?>
			<div class="ncah-form-note ncah-form-note--err" role="alert"><?php echo esc_html( $msg ); ?>
			<?php if ( 'member' === $status ) : ?> <a href="<?php echo esc_url( $join ); ?>">Register as a member</a><?php endif; ?></div>
		<?php endif; ?>
		<input type="hidden" name="action" value="ncah_business_apply">
		<?php wp_nonce_field( 'ncah_business_apply', 'ncah_nonce' ); ?>
		<input type="hidden" name="ncah_t" value="<?php echo esc_attr( time() ); ?>">
		<p class="ncah-hp" aria-hidden="true"><label>Leave this empty <input type="text" name="ncah_site" tabindex="-1" autocomplete="off"></label></p>

		<fieldset class="ncah-biz-member">
			<legend>Are you a registered NCAH member? <span aria-hidden="true">*</span></legend>
			<label class="ncah-radio"><input type="radio" name="member" value="yes" required> Yes, I am a registered member</label>
			<label class="ncah-radio"><input type="radio" name="member" value="no"> No, not yet</label>
			<div class="ncah-biz-join" hidden>
				<p><strong>Membership is required to be listed.</strong> Please register as a member first, then come back to request your listing.</p>
				<p><a class="wp-block-button__link wp-element-button has-white-color has-ncah-red-background-color has-text-color has-background" href="<?php echo esc_url( $join ); ?>">Register as a member</a></p>
			</div>
		</fieldset>

		<div class="ncah-biz-fields">
			<p><label for="biz-name">Business name <span aria-hidden="true">*</span></label>
				<input id="biz-name" name="business_name" type="text" autocomplete="organization" required></p>

			<p><label for="biz-reg">Is the business registered? <span aria-hidden="true">*</span></label>
				<select id="biz-reg" name="reg_status" required>
					<option value="">Select</option>
					<?php foreach ( ncah_dir_reg_options() as $k => $l ) : ?><option value="<?php echo esc_attr( $k ); ?>"><?php echo esc_html( $l ); ?></option><?php endforeach; ?>
				</select></p>

			<p><label for="biz-cat">Category <span aria-hidden="true">*</span></label>
				<select id="biz-cat" name="category" required>
					<option value="">Select</option>
					<?php if ( $terms && ! is_wp_error( $terms ) ) : foreach ( $terms as $t ) : ?><option value="<?php echo esc_attr( $t->term_id ); ?>"><?php echo esc_html( $t->name ); ?></option><?php endforeach; endif; ?>
				</select></p>

			<p><label for="biz-desc">Service or product description <span aria-hidden="true">*</span></label>
				<textarea id="biz-desc" name="description" rows="5" maxlength="600" required></textarea>
				<small>Up to 600 characters. This text appears in the directory.</small></p>

			<fieldset>
				<legend>Business address <span aria-hidden="true">*</span></legend>
				<p><label for="biz-street">Street address</label><input id="biz-street" name="street" type="text" autocomplete="address-line1" required></p>
				<div class="ncah-form-row">
					<p><label for="biz-city">City</label><input id="biz-city" name="city" type="text" autocomplete="address-level2" required></p>
					<p><label for="biz-prov">Province</label>
						<select id="biz-prov" name="province" autocomplete="address-level1">
							<?php foreach ( ncah_member_provinces() as $k => $l ) : ?><option value="<?php echo esc_attr( $k ); ?>"<?php selected( $k, 'ON' ); ?>><?php echo esc_html( $l ); ?></option><?php endforeach; ?>
						</select></p>
					<p><label for="biz-postal">Postal code</label><input id="biz-postal" name="postal" type="text" autocomplete="postal-code" placeholder="L8P 1A1" required></p>
				</div>
			</fieldset>

			<p><label for="biz-person">Contact person <span aria-hidden="true">*</span></label>
				<input id="biz-person" name="contact_person" type="text" autocomplete="name" required></p>

			<div class="ncah-form-row ncah-form-row--2">
				<p><label for="biz-phone">Phone <span aria-hidden="true">*</span></label>
					<input id="biz-phone" name="phone" type="tel" inputmode="tel" autocomplete="tel" placeholder="289 244 2568" required></p>
				<p><label for="biz-wa">WhatsApp number <span class="ncah-opt">(optional)</span></label>
					<input id="biz-wa" name="whatsapp" type="tel" inputmode="tel" placeholder="289 244 2568"></p>
			</div>

			<p><label for="biz-email">Email <span aria-hidden="true">*</span></label>
				<input id="biz-email" name="email" type="email" autocomplete="email" required></p>

			<p><label for="biz-web">Website <span class="ncah-opt">(optional)</span></label>
				<input id="biz-web" name="website" type="url" inputmode="url" placeholder="https://"></p>

			<p class="ncah-check"><label><input type="checkbox" name="consent" value="yes" required> I agree that NCAH may store these details and show the business name, description, address, contact person, phone, email and WhatsApp number publicly in the directory once approved, as described in the <a href="<?php echo esc_url( home_url( '/privacy-policy/' ) ); ?>">Privacy Policy</a>. <span aria-hidden="true">*</span></label></p>

			<p class="ncah-biz-note"><small>Every request is checked by an administrator against the member list before it is listed.</small></p>
			<p><button type="submit" class="wp-block-button__link wp-element-button has-white-color has-ncah-red-background-color has-text-color has-background">Request a listing</button></p>
		</div>
	</form>
	<script>
	( function () {
		var f = document.querySelector( '.ncah-bizform' ); if ( ! f ) { return; }
		var radios = f.querySelectorAll( 'input[name="member"]' ), join = f.querySelector( '.ncah-biz-join' ), fields = f.querySelector( '.ncah-biz-fields' );
		function sync() {
			var v = ( f.querySelector( 'input[name="member"]:checked' ) || {} ).value;
			join.hidden = v !== 'no';
			fields.hidden = v !== 'yes';
			fields.querySelectorAll( '[required]' ).forEach( function ( el ) { el.disabled = v !== 'yes'; } );
		}
		radios.forEach( function ( r ) { r.addEventListener( 'change', sync ); } ); sync();
	} )();
	</script>
	<?php
	return ob_get_clean();
} );

function ncah_dir_redirect( $code ) {
	$back = wp_get_referer() ?: home_url( '/business-directory/' );
	$back = remove_query_arg( 'ncah_biz', preg_replace( '/#.*$/', '', $back ) );
	wp_safe_redirect( add_query_arg( 'ncah_biz', $code, $back ) . '#request' );
	exit;
}

function ncah_dir_is_blacklisted( $name, $email ) {
	$q = new WP_Query( array(
		'post_type'      => 'ncah_business',
		'post_status'    => 'any',
		'posts_per_page' => 50,
		'meta_query'     => array( array( 'key' => 'directory_status', 'value' => 'blacklisted' ) ),
	) );
	foreach ( $q->posts as $p ) {
		if ( 0 === strcasecmp( $p->post_title, $name ) || 0 === strcasecmp( (string) get_post_meta( $p->ID, 'email', true ), $email ) ) {
			return true;
		}
	}
	return false;
}

function ncah_dir_handle() {
	if ( ! isset( $_POST['ncah_nonce'] ) || ! wp_verify_nonce( sanitize_text_field( wp_unslash( $_POST['ncah_nonce'] ) ), 'ncah_business_apply' ) ) {
		ncah_dir_redirect( 'spam' );
	}
	if ( ! empty( $_POST['ncah_site'] ) || ( time() - (int) ( $_POST['ncah_t'] ?? 0 ) ) < 4 ) {
		ncah_dir_redirect( 'spam' );
	}
	$ip  = 'ncah_biz_' . md5( (string) ( $_SERVER['REMOTE_ADDR'] ?? '' ) );
	$hit = (int) get_transient( $ip );
	if ( $hit >= 5 ) {
		ncah_dir_redirect( 'wait' );
	}
	if ( 'yes' !== ( $_POST['member'] ?? '' ) ) {
		ncah_dir_redirect( 'member' );
	}
	$g      = function ( $k ) { return sanitize_text_field( wp_unslash( $_POST[ $k ] ?? '' ) ); };
	$name   = $g( 'business_name' );
	$reg    = sanitize_key( $_POST['reg_status'] ?? '' );
	$cat    = absint( $_POST['category'] ?? 0 );
	$desc   = mb_substr( sanitize_textarea_field( wp_unslash( $_POST['description'] ?? '' ) ), 0, 600 );
	$street = $g( 'street' );
	$city   = $g( 'city' );
	$prov   = sanitize_text_field( wp_unslash( $_POST['province'] ?? 'ON' ) );
	$postal = strtoupper( $g( 'postal' ) );
	$person = $g( 'contact_person' );
	$email  = sanitize_email( wp_unslash( $_POST['email'] ?? '' ) );
	$web    = esc_url_raw( wp_unslash( $_POST['website'] ?? '' ) );
	if ( '' === $name || '' === $desc || '' === $street || '' === $city || '' === $person || ! isset( ncah_dir_reg_options()[ $reg ] ) || ! isset( ncah_member_provinces()[ $prov ] ) || empty( $_POST['consent'] ) || ! $cat || ! term_exists( $cat, 'business_category' ) ) {
		ncah_dir_redirect( 'missing' );
	}
	if ( ! is_email( $email ) ) {
		ncah_dir_redirect( 'email' );
	}
	$phone = ncah_member_normalise_phone( $g( 'phone' ) );
	if ( ! $phone ) {
		ncah_dir_redirect( 'phone' );
	}
	$wa = '';
	if ( '' !== $g( 'whatsapp' ) ) {
		$wa = ncah_member_normalise_phone( $g( 'whatsapp' ) );
		if ( ! $wa ) {
			ncah_dir_redirect( 'wa' );
		}
	}
	if ( ! preg_match( '/^[ABCEGHJ-NPRSTVXY]\d[ABCEGHJ-NPRSTV-Z][ -]?\d[ABCEGHJ-NPRSTV-Z]\d$/', $postal ) ) {
		ncah_dir_redirect( 'postal' );
	}
	$postal = substr( $postal, 0, 3 ) . ' ' . substr( preg_replace( '/[ -]/', '', $postal ), 3 );
	if ( ncah_dir_is_blacklisted( $name, $email ) ) {
		ncah_dir_redirect( 'spam' );
	}
	set_transient( $ip, $hit + 1, HOUR_IN_SECONDS );
	$id = wp_insert_post( array( 'post_type' => 'ncah_business', 'post_status' => 'publish', 'post_title' => $name ) );
	if ( ! $id || is_wp_error( $id ) ) {
		ncah_dir_redirect( 'spam' );
	}
	wp_set_object_terms( $id, array( $cat ), 'business_category' );
	$address = $street . ', ' . $city . ', ' . $prov . ' ' . $postal;
	foreach ( array( 'reg_status' => $reg, 'description' => $desc, 'address' => $address, 'contact_person' => $person, 'phone' => $phone, 'whatsapp' => $wa, 'email' => $email, 'website' => $web, 'directory_status' => 'pending', 'member_claimed' => 'yes', 'consent' => 'yes ' . gmdate( 'Y-m-d H:i' ) . ' UTC' ) as $k => $v ) {
		update_post_meta( $id, $k, $v );
	}
	$to   = get_option( 'ncah_member_notify', 'info@ncahamilton.ca' );
	$body = "New business directory request\n\nBusiness: $name\nRegistration: " . ncah_dir_reg_options()[ $reg ] . "\nContact: $person\nPhone: $phone\nWhatsApp: $wa\nEmail: $email\nAddress: $address\n\nVerify that the contact is a registered member, then approve or reject:\n" . admin_url( 'edit.php?post_type=ncah_business&dir_status=pending' );
	wp_mail( $to, 'New NCAH business directory request: ' . $name, $body );
	wp_mail( $email, 'NCAH business directory: request received', "Hello $person,\n\nWe received your request to list $name in the NCAH business directory. An administrator will verify your membership and details, and your business will appear in the directory once approved.\n\nYours in Service,\nNigerian Canadian Association, Hamilton and Environs\ninfo@ncahamilton.ca" );
	ncah_dir_redirect( 'ok' );
}
add_action( 'admin_post_nopriv_ncah_business_apply', 'ncah_dir_handle' );
add_action( 'admin_post_ncah_business_apply', 'ncah_dir_handle' );
