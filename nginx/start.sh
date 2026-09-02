#!/bin/sh
set -eu

CERTIFICATE="/etc/letsencrypt/live/${DOMAIN}/fullchain.pem"
ACTIVE_CONFIG=/etc/nginx/conf.d/default.conf

render_config() {
    template="$1"
    envsubst '${DOMAIN}' < "$template" > "${ACTIVE_CONFIG}.new"
    mv "${ACTIVE_CONFIG}.new" "$ACTIVE_CONFIG"
}

if [ -f "$CERTIFICATE" ]; then
    render_config /etc/nginx/source-templates/https.conf.template
else
    render_config /etc/nginx/source-templates/http.conf.template
fi

# Certbot runs in another container. Detect both the first certificate and
# renewals, then atomically switch/reload nginx without stopping the site.
(
    last_signature=""
    while sleep 5; do
        [ -f "$CERTIFICATE" ] || continue
        signature="$(stat -c '%Y:%s' "$CERTIFICATE")"
        [ "$signature" = "$last_signature" ] && continue
        render_config /etc/nginx/source-templates/https.conf.template
        if nginx -t; then
            nginx -s reload
            last_signature="$signature"
        fi
    done
) &

exec nginx -g 'daemon off;'
