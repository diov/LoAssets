using System.Net;
using System.Runtime.Serialization.Formatters.Binary;
using System.Text.Encodings.Web;
using System.Text.Json;
using Microsoft.Azure.Functions.Worker;
using Microsoft.Azure.Functions.Worker.Http;
using Microsoft.Extensions.Logging;

namespace Binser
{
  public class SerBin
  {
    private readonly ILogger _logger;

    public SerBin(ILoggerFactory loggerFactory)
    {
      _logger = loggerFactory.CreateLogger<SerBin>();
    }

    [Function("SerBin")]
    public HttpResponseData Run([HttpTrigger(AuthorizationLevel.Function, "post")] HttpRequestData req)
    {
      Dictionary<String, Object>? dict = null;
#pragma warning disable SYSLIB0011
      BinaryFormatter binFormatter = new BinaryFormatter();
      try
      {
        dict = binFormatter.Deserialize(req.Body) as Dictionary<String, Object>;
      }
      catch (Exception e)
      {
        _logger.LogError("Could not deserialize binary data to JSON: " + e.Message);
        return RespHandler.generateErrorResponse(req, e.Message);
      }
#pragma warning restore SYSLIB0011

      if (dict == null)
      {
        RespHandler.generateErrorResponse(req, "Deserialize an empty Dictionary");
      }


      var options = new JsonSerializerOptions();
      options.Encoder = JavaScriptEncoder.UnsafeRelaxedJsonEscaping;
      byte[] data = JsonSerializer.SerializeToUtf8Bytes(dict, options);

      var response = req.CreateResponse(HttpStatusCode.OK);
      response.Headers.Add("Content-Type", "application/json; charset=utf-8");
      response.WriteBytes(data);
      return response;
    }
  }
}
