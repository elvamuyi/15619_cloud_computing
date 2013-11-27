import java.io.IOException;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.hbase.HBaseConfiguration;
import org.apache.hadoop.hbase.client.Put;
import org.apache.hadoop.hbase.io.ImmutableBytesWritable;
import org.apache.hadoop.hbase.mapreduce.TableOutputFormat;
import org.apache.hadoop.hbase.util.Bytes;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.io.Writable;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;

import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;

public class PersistJsonToTweetTable {
  
  public static final String NAME = "persisit_json_to_tweet_table_in_hbase";
  public static final String TABLE = "tweet";
  public static final String[] FAMILY = {"time", "text", "user", "re"};
  public static final String[] QUALIFIER = {"time", "text", "uid", "is_re", "o_uid"};

  public static class PersistMapper extends Mapper<LongWritable, Text, ImmutableBytesWritable, Writable> {
    
    private JSONParser parser = new JSONParser();

    public void map(LongWritable offset, Text line, Context context) throws IOException {
      try {
      
        /* Extract related fields from JSON object */
        JSONObject tweet = (JSONObject) parser.parse(line.toString());      // JSON object Tweets
        String tid = (String) tweet.get("id_str");                          // tweet id
        String time = (String) tweet.get("created_at");                     // time of creation
        String text = (String) tweet.get("text");                           // text
        JSONObject user = (JSONObject) tweet.get("user");                   // JSON object Users
        String uid = (String) user.get("id_str");                           // user id
        JSONObject o_tweet = (JSONObject) tweet.get("retweeted_status");    // if is retweet, get user id of original tweet
        String o_uid = "none";
        Boolean is_re = false;
        if (o_tweet != null) {
          is_re = true;
          JSONObject o_user = (JSONObject) o_tweet.get("user");
          o_uid = (String) o_user.get("id_str");
        }

        Put put = new Put(Bytes.toBytes(tid));  // use tweet id as row key
        put.add(Bytes.toBytes(FAMILY[0]), Bytes.toBytes(QUALIFIER[0]), Bytes.toBytes(time));  // Column Family: time, Column: time, Value: time
        put.add(Bytes.toBytes(FAMILY[1]), Bytes.toBytes(QUALIFIER[1]), Bytes.toBytes(text));  // Column Family: text, Column: text, Value: text
        put.add(Bytes.toBytes(FAMILY[2]), Bytes.toBytes(QUALIFIER[2]), Bytes.toBytes(uid));   // Column Family: user, Column: uid, Value: uid
        put.add(Bytes.toBytes(FAMILY[3]), Bytes.toBytes(QUALIFIER[3]), new byte[]{(byte) (is_re?1:0)}); // Column Family: re, Column: is_re, Value: is_re
        put.add(Bytes.toBytes(FAMILY[3]), Bytes.toBytes(QUALIFIER[4]), Bytes.toBytes(o_uid)); // Column Family: re, Column: o_uid, Value: o_uid
        context.write(new ImmutableBytesWritable(Bytes.toBytes(tid)), put);
        
      } catch (Exception e) {
        e.printStackTrace();
      }
    }
  }
  
  public static void main(String[] args) throws Exception {
    Configuration conf = HBaseConfiguration.create();
    Job job = new Job(conf, NAME);
    job.setJarByClass(PersistJsonToTweetTable.class);
    job.setMapperClass(PersistMapper.class);
    job.setOutputFormatClass(TableOutputFormat.class);
    job.getConfiguration().set(TableOutputFormat.OUTPUT_TABLE, TABLE);
    job.setOutputKeyClass(ImmutableBytesWritable.class);
    job.setOutputValueClass(Writable.class);
    job.setNumReduceTasks(0);
    FileInputFormat.addInputPath(job, new Path(args[0])); // first argument is the input file path

    System.exit(job.waitForCompletion(true) ? 0 : 1);
  }
}
