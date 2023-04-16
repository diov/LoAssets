using System.Net;
using System.Text.Encodings.Web;
using System.Text.Json;
using Microsoft.Azure.Functions.Worker.Http;

namespace Binser
{
  public class RespHandler
  {
    public static HttpResponseData generateErrorResponse(HttpRequestData req, String message)
    {
      var response = req.CreateResponse(HttpStatusCode.BadRequest);
      var options = new JsonSerializerOptions();
      options.Encoder = JavaScriptEncoder.UnsafeRelaxedJsonEscaping;
      var result = JsonSerializer.SerializeToUtf8Bytes(new Dictionary<String, String>() {
        {"error", message},
      }, options);

      response.Headers.Add("Content-Type", "application/json; charset=utf-8");
      response.WriteBytes(result);
      return response;
    }
  }
}
