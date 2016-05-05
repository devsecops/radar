#!/usr/bin/env ruby

# securitychecker
# Description: Validate security of CloudFormation templates

require 'optparse'
require 'ostruct'
require 'json'
require 'pry'

version = '0.3 (Ruby)'
USAGE = %(Usage:
securitychecker --template <CF-Template> --config <Test Config> [ --unit-test ] --output <outputfile>

Options:
  -v, --version                             Show program version number and exit
  -h, --help                                Show this help message and exit
  -t TEMPLATE, --template=TEMPLATE          CloudFormation template to test
  -u TEST, --unit-test=TEST                 Unittest, if specifying a single
                                            unit test file
  -c CONFIG, --config=CONFIG                Config file, if specifying a test
                                            config file for multiple tests
  -o OUTFILE, --output=OUTFILE              Output file
  -l CONFIGTYPE, --list-config=CONFIGTYPE   List configurations available with
                                            this install
).freeze

# Handle arguments passed to the script
class SCOpts
  def self.parse(args)
    opts = OpenStruct.new
    opts.action = 'store'
    opts.template = 'main.json'
    opts.dest = nil
    opts.configtype = nil
    opts.updatefile = nil
    opts.unittest = nil

    parser = OptionParser.new do |o|
      o.on('-t', '--template template') do |t|
        opts.dest = 'template'
        opts.template = t
      end

      o.on('-u', '--unit-test unittest') do |u|
        opts.dest = 'test'
        opts.unittest = u
      end

      o.on('-c', '--config') do
        opts.dest = 'config'
      end

      o.on('-o', '--output') do
        opts.dest = 'outfile'
      end

      o.on('-l', '--list-config configtype') do |l|
        opts.dest = 'configtype'
        opts.configtype = l
      end

      o.on('-b', '--bool') do
        opts.action = 'store_true'
      end

      o.on('-p', '--update') do |u|
        opts.updatefile = u
      end

      o.on('-v', '--version') do
        opts.dest = 'version'
      end

      o.on('-r', '--region') do |r|
        opts.dest = r || 'us-east-1'
      end

      o.on('-h', '--help') do
        opts.dest = 'help'
      end
    end

    begin
      parser.parse!(args)
    rescue Exception => e
      $stderr.puts "#{e.message}\n"
    end
    opts
  end
end

def print_usage(msg)
  puts "#{msg}\n\n"
  puts USAGE
end

options = SCOpts.parse(ARGV)
case options.dest
when 'version'
  puts "securitychecker #{version}"
  exit
when 'help'
  print_usage "Help for securitychecker #{version}"
  exit
# Option to display current config for installed securitycheck
when 'configtype'
  if options.configtype == 'compliance'
    # Need to make print_compliance method and run it here
  elsif options.configtype == 'unittests'
    # Need to make print_unittests method and run it here
  else
    print_usage "Error:\n-l, --list-config: Single unit test to check\n"\
                "Takes values: [ compliance | unittests ]\n"
    exit
  end
  # Attempt to update if option provided
  if options.updatefile
    if options.template == 'main.json'
      puts 'Using default template: main.json'
      puts 'You can specify a template with -t or --template'
    end
    # Need to make update method and run it here
    exit
  end

  # Read JSON from CloudFormation template
  # cftemplate = File.open(options.template, 'r')
  # cftemplate = JSON.parse!(cftemplate)
else
  print_usage 'Invalid options or values specified. Try -h for help'
end
