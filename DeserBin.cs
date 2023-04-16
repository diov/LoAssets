using System.Net;
using System.Runtime.Serialization.Formatters.Binary;
using System.Text.Encodings.Web;
using System.Text.Json;
using Microsoft.Azure.Functions.Worker;
using Microsoft.Azure.Functions.Worker.Http;
using Microsoft.Extensions.Logging;

namespace Binser
{
  public class DeserBin
  {
    private readonly ILogger _logger;

    public DeserBin(ILoggerFactory loggerFactory)
    {
      _logger = loggerFactory.CreateLogger<DeserBin>();
    }

    [Function("DeserBin")]
    public HttpResponseData Run([HttpTrigger(AuthorizationLevel.Function, "post")] HttpRequestData req)
    {
      var options = new JsonSerializerOptions();
      options.Encoder = JavaScriptEncoder.UnsafeRelaxedJsonEscaping;

      Dictionary<String, String>? jsonDict = null;
      try
      {
        jsonDict = JsonSerializer.Deserialize<Dictionary<String, String>>(req.Body, options);
      }
      catch (Exception e)
      {
        _logger.LogError("Could not deserialize JSON: " + e.Message);
        return RespHandler.generateErrorResponse(req, e.Message);
      }

      if (jsonDict == null)
      {
        _logger.LogError("Deserialize an empty JSON");
        return RespHandler.generateErrorResponse(req, "Deserialize an empty JSON");
      }

      // LO TextAsset is a BinaryFormatter serialized Dictionary<String, Object>
      Dictionary<String, Object> dict = jsonDict.ToDictionary(
        kvp => kvp.Key,
        kvp => (Object)kvp.Value
      );

      var response = req.CreateResponse(HttpStatusCode.OK);
      response.Headers.Add("Content-Type", "application/octet-stream");
#pragma warning disable SYSLIB0011
      BinaryFormatter binFormatter = new BinaryFormatter();
      try
      {
        binFormatter.Serialize(response.Body, dict);
      }
      catch (Exception e)
      {
        _logger.LogError("Could not serialize JSON to binary data: " + e.Message);
        return RespHandler.generateErrorResponse(req, e.Message);
      }
#pragma warning restore SYSLIB0011      

      return response;
    }
  }
}
