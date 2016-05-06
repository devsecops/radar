require 'yaml'
require 'optparse'

def check_options (opts)
  options_okay = true

  if opts[:bucket_name].nil?
    puts "S3 Bucket Name is required!"
    options_okay = false
  elsif opts[:object_key].nil?
    puts "Object Key is required!"
    options_okay = false
  elsif opts[:file_name].nil?
    puts "Deploy YAML File Name is required!"
    options_okay = false
  end 

  return options_okay
end

def audit_file (opts)

  if File.exist?(opts[:file_name])
    thing = YAML.load_file(opts[:file_name])

    #puts thing.flatten.inspect
    aws_region  = thing["labels"]["master"]["config"]["aws_region"]
    bucket_name = thing["labels"]["master"]["config"]["bucket_name"]
    object_key = thing["labels"]["master"]["config"]["object_key"]
 
    if !aws_region.downcase.eql? opts[:aws_region].downcase 
      puts "AWS Region does not match!"
    elsif !bucket_name.downcase.eql? opts[:bucket_name].downcase 
      puts "S3 Bucket Name does not match!"
    elsif !object_key.downcase.eql? opts[:object_key].downcase 
      puts "Object Key does not match!"
    else
      puts "#{opts[:file_name]} contents match input parameters"
   end

  else
    puts "YAML file #{opts[:file_name]} does not exist!"
  end
end

##### Main #####

options = {:aws_region => 'US-WEST-2', :bucket_name => nil, :object_key => nil, :file_name => nil }
parser = OptionParser.new do|opts|
  opts.banner = "Usage: yaml_auditor.rb [options]"

  opts.on('-r', '--aws_region REGION', 'Input AWS Region. default: US-WEST-2') { |o| options[:aws_region] = o }
  opts.on('-b', '--bucket_name BUCKET', 'S3 Bucket Name.') { |o| options[:bucket_name] = o }
  opts.on('-o', '--object_key OBJECT_KEY', 'Object Key.') { |o| options[:object_key] = o }
  opts.on('-f', '--file_name FILE_NAME', 'YAML File Name.') { |o| options[:file_name] = o }
  opts.on('-h', '--help', 'Displays Help') do
    puts opts
    exit
  end
end

parser.parse!

if check_options (options)
  # puts "AWS Region: #{options[:aws_region]}"
  # puts "S3 Bucket Name: #{options[:bucket_name]}"
  # puts "Object Key: #{options[:object_key]}"
  # puts "Deploy YAML File Name: #{options[:file_name]}"

  audit_file (options)
end
