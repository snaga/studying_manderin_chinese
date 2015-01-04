SET PATH=C:\bin;%PATH%

cf set-env studying-mandarin-chinese JBP_LOG_LEVEL DEBUG 
cf files studying-mandarin-chinese app/.buildpack-diagnostics/buildpack.log
cf files studying-mandarin-chinese logs/env.log
cf files studying-mandarin-chinese logs/staging_task.log

cf push studying-mandarin-chinese -m 512M -b https://github.com/cloudfoundry/cf-buildpack-python.git -c "python server.py"

