#!/usr/bin/env perl

use strict;
use warnings;
use Getopt::Long;

#
# bed2faidxsta.pl
# --
# Reads BED data from standard input, writes FASTA to standard output.
#
# Dependent on samtools and indexed FASTA data files located in $fastaDir 
# variable. Set --fastaDir=dir to set custom directory containing a source 
# of per-build, bgzip-compressed FASTA and associated index (fa.gz.fai) 
# files, or leave unset to use data in current working directory. Use the
# --fastaIsUncompressed option if the FASTA files are not compressed.
#

# test if samtools is available
`samtools --version` || die "Error: The samtools application is required to run this script. Try 'module add samtools' or install a local copy of samtools.\n";

# default FASTA input is current working directory
my $fastaDir = `pwd`; chomp $fastaDir;
# default is to assume input coordinates use zero-based index scheme
my $oneBased;
# default is to leave IDs alone
my $useIDPrefixAsStrand;
# default is to assume FASTA files are bgzip-compressed
my $fastaIsUncompressed;

GetOptions ('fastaDir=s' => \$fastaDir, 'oneBased' => \$oneBased, 'useIDPrefixAsStrand' => \$useIDPrefixAsStrand, 'fastaIsUncompressed' => \$fastaIsUncompressed);

if (! -d $fastaDir) { die "Error: FASTA directory does not exist\n"; }

while (<STDIN>) {
    chomp;
    my ($chr, $start, $stop, $id, $score, $strand) = split("\t", $_);
    if (!defined($chr) || !defined($start) || !defined($stop)) { die "Error: No chromosome name, start or stop position defined\n"; }
    if (!defined($id)) { $id = "."; }
    if (!defined($score)) { $score = "."; }
    if (!defined($strand)) { $strand = "+"; } else { $strand = substr($strand, 0, 1); }
    # adjust coordinates to one-based index, if necessary
    my ($queryChr, $queryStart, $queryStop) = ($chr, $start, $stop);
    if (!$oneBased) {
        $queryStart++;
    }
    # adjust strand if required
    if ($useIDPrefixAsStrand) {
        $strand = substr($id, 0, 1);
    }
    # lookup
    my $queryFn = "$fastaDir/$chr.fa.gz";
    if ($fastaIsUncompressed) {
        $queryFn = "$fastaDir/$chr.fa";
    }
    my $queryKey = "$queryChr:$queryStart-$queryStop";
    my $queryResult = `samtools faidx $queryFn $queryKey`; chomp $queryResult; 
    # linearize result
    my @lines = split("\n", $queryResult);
    my @seqs = @lines[1..(scalar @lines - 1)];
    my $seq = join("", @seqs);
    # handle reverse-stranded elements
    if ($strand eq "-") {
        $seq = rc_sequence($seq);
    }
    # print to standard output
    my $header = ">".join(":",($chr, $start, $stop, $id, $score, $strand));
    print STDOUT $header."\n".$seq."\n";
}

sub rc_sequence {
    my $seq = shift @_;
    my $reverse_complement = reverse($seq);
    $reverse_complement =~ tr/ACGTacgt/TGCAtgca/;
    return $reverse_complement;
}
