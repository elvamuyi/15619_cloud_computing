import java.io.IOException;
import java.util.HashSet;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.hbase.HBaseConfiguration;
import org.apache.hadoop.hbase.client.Put;
import org.apache.hadoop.hbase.client.Result;
import org.apache.hadoop.hbase.client.Scan;
import org.apache.hadoop.hbase.io.ImmutableBytesWritable;
import org.apache.hadoop.hbase.mapreduce.TableMapReduceUtil;
import org.apache.hadoop.hbase.mapreduce.TableMapper;
import org.apache.hadoop.hbase.mapreduce.TableReducer;
import org.apache.hadoop.hbase.util.Bytes;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;

public class AddReUsersToUserTable {
  
  public static final String NAME = "add_re_user_list_to_user_table_in_hbase";
  
  public static final String INPUT_TABLE = "tweet";
  public static final String OUTPUT_TABLE = "user";
  public static final byte[] USER = "user".getBytes();
  public static final byte[] UID = "uid".getBytes();
  public static final byte[] RE = "re".getBytes();
  public static final byte[] IS_RE = "is_re".getBytes();
  public static final byte[] O_UID = "o_uid".getBytes();
  public static final byte[] RE_UIDS = "re_uids".getBytes();

  public static class HbaseTableMapper extends TableMapper<Text, Text> {
    
    private Text user_id = new Text();
    private Text re_uid = new Text();
    
    public void map(ImmutableBytesWritable row, Result columns, Context context) throws IOException, InterruptedException {
      Boolean is_re = columns.getValue(RE, IS_RE)[0] != 0;  // get value in column "re:is_re"
      if (is_re) {
        String uid = new String(columns.getValue(USER, UID));     // get value in column "user:uid"
        String o_uid = new String(columns.getValue(RE, O_UID));;  // get value in column "re:o_uid"

        user_id.set(o_uid);
        re_uid.set(uid);
        context.write(user_id, re_uid);
      }
    }
  }
  
  public static class HbaseTableReducer extends TableReducer<Text, Text, ImmutableBytesWritable> {
    
    public void reduce(Text key, Iterable<Text> values, Context context) throws IOException, InterruptedException {
      HashSet<String> re_user_set = new HashSet<String>();  // use a hashset to remove duplicates
      for (Text value : values) {
        String user = value.toString();
        re_user_set.add(user);
      }
      
      String re_users = "";
      for (String user : re_user_set) {
        if (user != "none") re_users += user + "\n";
      }
      
      Put put = new Put(Bytes.toBytes(key.toString()));   // use user id as row key
      put.add(RE, RE_UIDS, Bytes.toBytes(re_users));      // Column Family: re, Column: re_uids, Value: re_users
      context.write(null, put);
    }
  }
  
  public static void main(String[] args) throws Exception {
    Configuration conf = HBaseConfiguration.create();
    Job job = new Job(conf, NAME);
    job.setJarByClass(AddReUsersToUserTable.class);
    
    Scan scan = new Scan();
    scan.setCaching(500);        // 1 is the default in Scan, which will be bad for MapReduce jobs
    scan.setCacheBlocks(false);  // don't set to true for MR jobs
    
    TableMapReduceUtil.initTableMapperJob(INPUT_TABLE, scan, HbaseTableMapper.class, Text.class, Text.class, job);
    TableMapReduceUtil.initTableReducerJob(OUTPUT_TABLE, HbaseTableReducer.class, job);
    
    System.exit(job.waitForCompletion(true) ? 0 : 1);
  }
}
