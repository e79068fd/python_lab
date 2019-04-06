#/!/usr/bin/perl
use strict;
use warnings;
use List::Util qw[min max];

my %ip_addr = ();
while(<>) {
    /((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?))/;
    if(exists($ip_addr{"$1"})) {
        $ip_addr{"$1"}++;
    } else {
        $ip_addr{"$1"} = 1;
    }
};

my $i = 1;
my @sorted_ip_addr = sort {-$ip_addr{$a} <=> -$ip_addr{$b}} keys %ip_addr;
my $stop = min(10, scalar(@sorted_ip_addr));
while($i <= $stop){
    my $key = $sorted_ip_addr[$i - 1];
    my $value = $ip_addr{$key};
    print "$i: $key => $value\n";
    $i++;
};
