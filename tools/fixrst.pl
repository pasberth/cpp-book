#!/usr/bin/perl -i -nl

if ( /^<p>$/ || /^<\/p>$/ ) {
} else {
    s/^(\s*)<p>/$1/;
    s/<\/p>(\s*)$/$1/;
    print $_;
}