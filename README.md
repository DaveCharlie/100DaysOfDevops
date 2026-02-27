# 100DaysOfDevops
Understanding Devops 

Script Execution Permissions

Question 
In a bid to automate backup processes, the xFusionCorp Industries sysadmin team has developed a new bash script named xfusioncorp.sh. While the script has been distributed to all necessary servers, it lacks executable permissions on App Server 3 within the Stratos Datacenter.
Your task is to grant executable permissions to the /tmp/xfusioncorp.sh script on App Server 3. Additionally, ensure that all users have the capability to execute it.

Solution : 
sudo chmod a+rx /tmp/xfusioncorp.sh

Why this is necessary
In Linux, scripts require explicit execute (x) permission to run as standalone programs. Additionally, because bash is an interpreter, it must be able to read (r) the file to process the commands within it, which is why +rx is often preferred over just +x
