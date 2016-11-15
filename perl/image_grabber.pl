#!/usr/bin/perl

use strict;
use LWP::UserAgent; 
use LWP::Simple;
use HTTP::Request;
require HTML::TreeBuilder;
require URI::URL;

my ($url, $mydir) = @ARGV;
$| = 1;

my $ua = LWP::UserAgent->new;
$ua->timeout(10000);
my $st = 1;

print("$mydir\n");
print("$url\n");
mkdir $mydir;

#my $url = "https://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Daps&field-keywords=watches";
my $referer = $url;
my $request = HTTP::Request->new(GET => $url);
$request->referer($referer);
my $response = $ua->request($request);
my $content = $response->decoded_content;
my $flag = 0;
while ( $flag == 0 ) {
if($response->is_success) {
	my @link;
	$flag = 1;
	print " Here... \n";
	my $page = $response->decoded_content;
	my $base_url = $response->base;
	my $parser = new HTML::TreeBuilder;
	$parser->parse($response->content);
	$parser->eof;
	foreach (@{$parser->extract_links(qw(img))}) {
		push @link, URI::URL::url($$_[0])->abs($base_url)->as_string;
	}
	$parser->delete;
	my $count = 1;
	foreach (@link) {
		if ( $_ =~ m/.*\.jpg/i || $_ =~ m/.*\.png/i ) {
			getstore($_, "$mydir/$count");
			$count++;
			print ("$_\n");
		}
	}
	
	print ( "Base url is $base_url\n");
	if(open(CONTENTFILE, ">./$mydir/html")) {
		binmode(CONTENTFILE, ":utf8");
		print CONTENTFILE $page;
		close(CONTENTFILE);
	}
	else {
		print "failed to retrieve $url\n";
	}

}
else {
	if($response->code==503) {
		++$st;
		print " Out of time... \n";
	}
	else {
		last;
	}
}
#++$page;
sleep($st);
}
