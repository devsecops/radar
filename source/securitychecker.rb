#!/usr/bin/env ruby

# securitychecker
# Description: Validate security of CloudFormation templates

require 'optparse'
require 'ostruct'
require 'json'
require 'hashdiff'

version = '0.3 (Ruby)'
USAGE = %(Usage:
securitychecker --template <CF-Template> --baseline <CF-Template>

Options:
  -v, --version                             Show program version number and exit
  -h, --help                                Show this help message and exit
  -t TEMPLATE, --template=TEMPLATE          CloudFormation template to test
  -b TEMPLATE, --baseline=TEMPLATE          CloudFormation template to test
                                            against
)

# Handle arguments passed to the script
class SCOpts
  def self.parse(args)
    opts = OpenStruct.new

    parser = OptionParser.new do |o|
      o.on('-t', '--template template') do |t|
        opts.template = t
      end

      o.on('-b', '--baseline baseline') do |b|
        opts.baseline = b
      end

      o.on('-v', '--version') do
        opts.dest = 'version'
      end

      o.on('-h', '--help') do
        opts.dest = 'help'
      end
    end

    begin
      parser.parse!(args)
    rescue => e
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
when 'help'
  print_usage "Help for securitychecker #{version}"
else
  begin
    if options.template && options.baseline
      template = JSON.parse(File.read(options.template))
      baseline = JSON.parse(File.read(options.baseline))
      diff = HashDiff.diff(baseline, template)
      if diff.empty?
        puts 'Template matches baseline template.'
      else
        puts 'Found the following differences: '
        diff.each do |d|
          puts d.join(' ')
        end
        exit(2)
      end
    else
      print_usage 'Invalid options or values specified. Try -h for help'
      exit(1)
    end
  rescue => e
    puts e.message
    exit(1)
  end
end

exit(0)
